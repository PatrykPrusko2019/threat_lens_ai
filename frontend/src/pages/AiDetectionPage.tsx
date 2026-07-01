import axios from "axios";
import { useMutation } from "@tanstack/react-query";
import {
    BrainCircuit,
    Network,
    RotateCcw,
    ScanSearch,
    ShieldAlert,
    ShieldCheck,
} from "lucide-react";
import { useState } from "react";

import { runDetection } from "../api/detectionApi";
import type {
    DetectionModule,
    DetectionRequest,
    DetectionResponse,
} from "../types/detection";

type FraudPreset = "normal" | "suspicious" | "high-risk";
type NetworkPreset = "normal" | "suspicious" | "attack";

type FraudFormState = {
    amount: string;
    failedLogins: string;
    accountAgeDays: string;
    transactionVelocity: string;
    foreignTransaction: boolean;
};

type NetworkFormState = {
    sourceIp: string;
    destinationIp: string;
    protocol: string;
    duration: string;
    bytesSent: string;
    bytesReceived: string;
    packetsSent: string;
    packetsReceived: string;
};

const fraudPresets: Record<FraudPreset, FraudFormState> = {
    normal: {
        amount: "120",
        failedLogins: "0",
        accountAgeDays: "900",
        transactionVelocity: "2",
        foreignTransaction: false,
    },
    suspicious: {
        amount: "1800",
        failedLogins: "3",
        accountAgeDays: "40",
        transactionVelocity: "12",
        foreignTransaction: true,
    },
    "high-risk": {
        amount: "5000",
        failedLogins: "8",
        accountAgeDays: "5",
        transactionVelocity: "25",
        foreignTransaction: true,
    },
};

const networkPresets: Record<NetworkPreset, NetworkFormState> = {
    normal: {
        sourceIp: "192.168.1.10",
        destinationIp: "10.0.0.5",
        protocol: "tcp",
        duration: "1.5",
        bytesSent: "1200",
        bytesReceived: "2400",
        packetsSent: "20",
        packetsReceived: "25",
    },
    suspicious: {
        sourceIp: "192.168.1.20",
        destinationIp: "10.0.0.8",
        protocol: "tcp",
        duration: "3.2",
        bytesSent: "250000",
        bytesReceived: "1200",
        packetsSent: "5000",
        packetsReceived: "300",
    },
    attack: {
        sourceIp: "192.168.1.10",
        destinationIp: "10.0.0.5",
        protocol: "tcp",
        duration: "1.5",
        bytesSent: "6000000",
        bytesReceived: "80",
        packetsSent: "60000",
        packetsReceived: "20",
    },
};

function formatJson(value: unknown) {
    return JSON.stringify(value, null, 2);
}

function getRequestErrorMessage(error: unknown) {
    if (axios.isAxiosError(error)) {
        const detail = error.response?.data?.detail;

        if (typeof detail === "string") {
            return detail;
        }

        if (Array.isArray(detail)) {
            return detail
                .map((item) => {
                    const location = Array.isArray(item?.loc)
                        ? item.loc.join(".")
                        : "field";

                    return `${location}: ${item?.msg ?? "Invalid value"}`;
                })
                .join(" ");
        }

        return "Detection request failed. Check input data.";
    }

    return "Detection request failed. Try again.";
}

function isValidIp(value: string) {
    const parts = value.split(".");

    if (parts.length !== 4) {
        return false;
    }

    return parts.every((part) => {
        const numberValue = Number(part);
        return (
            part.trim() !== "" &&
            Number.isInteger(numberValue) &&
            numberValue >= 0 &&
            numberValue <= 255
        );
    });
}

function parseNonNegativeNumber(value: string, fieldName: string) {
    if (value.trim() === "") {
        throw new Error(`${fieldName} is required.`);
    }

    const numberValue = Number(value);

    if (!Number.isFinite(numberValue)) {
        throw new Error(`${fieldName} must be a valid number.`);
    }

    if (numberValue < 0) {
        throw new Error(`${fieldName} cannot be negative.`);
    }

    return numberValue;
}

function parseNonNegativeInteger(value: string, fieldName: string) {
    const numberValue = parseNonNegativeNumber(value, fieldName);

    if (!Number.isInteger(numberValue)) {
        throw new Error(`${fieldName} must be an integer.`);
    }

    return numberValue;
}

function buildFraudPayload(form: FraudFormState): DetectionRequest {
    const amount = parseNonNegativeNumber(form.amount, "Amount");
    const failedLogins = parseNonNegativeInteger(
        form.failedLogins,
        "Failed login attempts",
    );
    const accountAgeDays = parseNonNegativeInteger(
        form.accountAgeDays,
        "Account age",
    );
    const transactionVelocity = parseNonNegativeNumber(
        form.transactionVelocity,
        "Transaction velocity",
    );

    const riskPoints =
        (amount >= 3000 ? 35 : amount >= 1000 ? 20 : 0) +
        (failedLogins >= 6 ? 25 : failedLogins >= 3 ? 15 : 0) +
        (accountAgeDays <= 10 ? 20 : accountAgeDays <= 60 ? 10 : 0) +
        (transactionVelocity >= 20 ? 15 : transactionVelocity >= 10 ? 8 : 0) +
        (form.foreignTransaction ? 10 : 0);

    /*
     * The fraud model is an IsolationForest trained on 30 numeric credit-card features.
     * The short UI form is mapped into demo-friendly synthetic feature profiles:
     * - low risk -> normal vector
     * - medium risk -> suspicious but usually below fraud threshold
     * - high risk -> clear anomaly vector
     */
    const profileValue = riskPoints >= 80 ? 10 : riskPoints >= 45 ? 1 : 0;

    const features = Array(30).fill(profileValue) as number[];

    features[0] = profileValue;
    features[1] = profileValue;
    features[2] = profileValue;
    features[3] = form.foreignTransaction ? profileValue : 0;
    features[4] = profileValue;
    features[5] = failedLogins >= 3 ? profileValue : 0;
    features[6] = accountAgeDays <= 60 ? profileValue : 0;
    features[7] = transactionVelocity >= 10 ? profileValue : 0;
    features[8] = amount >= 1000 ? profileValue : 0;
    features[9] = form.foreignTransaction ? profileValue : 0;

    /*
     * The last feature is mapped from amount, but capped so the demo profile
     * remains stable and predictable for the IsolationForest model.
     */
    features[29] = riskPoints >= 80 ? 5000 : riskPoints >= 45 ? 1800 : 120;

    return {
        features,
    };
}

function buildNetworkPayload(form: NetworkFormState): DetectionRequest {
    if (!isValidIp(form.sourceIp)) {
        throw new Error("Source IP must be a valid IPv4 address.");
    }

    if (!isValidIp(form.destinationIp)) {
        throw new Error("Destination IP must be a valid IPv4 address.");
    }

    const protocol = form.protocol.trim().toLowerCase();

    if (!["tcp", "udp", "icmp"].includes(protocol)) {
        throw new Error("Protocol must be tcp, udp, or icmp.");
    }

    return {
        source_ip: form.sourceIp.trim(),
        destination_ip: form.destinationIp.trim(),
        protocol,
        duration: parseNonNegativeNumber(form.duration, "Duration"),
        bytes_sent: parseNonNegativeInteger(form.bytesSent, "Bytes sent"),
        bytes_received: parseNonNegativeInteger(
            form.bytesReceived,
            "Bytes received",
        ),
        packets_sent: parseNonNegativeInteger(form.packetsSent, "Packets sent"),
        packets_received: parseNonNegativeInteger(
            form.packetsReceived,
            "Packets received",
        ),
    };
}

type ResultPanelProps = {
    result: DetectionResponse | null;
    isPending: boolean;
};


function getDetectionSummary(result: DetectionResponse | null) {
    if (!result) {
        return null;
    }

    const data = result as Record<string, unknown>;

    if (data.fraud === true) {
        return {
            title: "Fraud detected",
            description: "High-risk transaction pattern detected by the fraud model.",
            tone: "danger",
        };
    }

    if (data.fraud === false) {
        return {
            title: "No fraud detected",
            description: "The transaction profile is currently below the fraud threshold.",
            tone: "success",
        };
    }

    if (data.intrusion === true) {
        return {
            title: "Intrusion detected",
            description: "A security event and alert were created for this network activity.",
            tone: "danger",
        };
    }

    if (data.intrusion === false) {
        return {
            title: "No intrusion detected",
            description: "The traffic did not cross the configured intrusion threshold.",
            tone: "success",
        };
    }

    if (data.anomaly === true) {
        return {
            title: "Network anomaly detected",
            description: "The autoencoder detected abnormal network behavior.",
            tone: data.severity === "critical" ? "danger" : "warning",
        };
    }

    if (data.anomaly === false) {
        return {
            title: "No anomaly detected",
            description: "Normal traffic detected. No security event or alert was created.",
            tone: "success",
        };
    }

    return null;
}


function ResultPanel({ result, isPending }: ResultPanelProps) {
    const summary = getDetectionSummary(result);

    const summaryClassName =
        summary?.tone === "danger"
            ? "border-red-500/30 bg-red-500/10 text-red-200"
            : summary?.tone === "warning"
              ? "border-amber-500/30 bg-amber-500/10 text-amber-200"
              : "border-emerald-500/30 bg-emerald-500/10 text-emerald-200";

    return (
        <div>
            <p className="mb-2 text-sm font-medium text-slate-300">
                Detection result
            </p>

            <div className="min-h-64 rounded-xl border border-slate-800 bg-slate-950 p-4">
                {!result && !isPending && (
                    <p className="text-sm text-slate-500">
                        Run detection to see backend model output here.
                    </p>
                )}

                {isPending && (
                    <p className="text-sm text-cyan-300">
                        Running detection module...
                    </p>
                )}

                {summary && (
                    <div
                        className={`mb-4 rounded-xl border px-4 py-3 ${summaryClassName}`}
                    >
                        <p className="text-sm font-semibold">{summary.title}</p>
                        <p className="mt-1 text-xs opacity-90">
                            {summary.description}
                        </p>
                    </div>
                )}

                {result && (
                    <pre className="overflow-auto whitespace-pre-wrap text-xs text-slate-200">
                        {formatJson(result)}
                    </pre>
                )}
            </div>
        </div>
    );
}

type FieldProps = {
    label: string;
    value: string;
    onChange: (value: string) => void;
    placeholder?: string;
};

function TextField({ label, value, onChange, placeholder }: FieldProps) {
    return (
        <div>
            <label className="text-sm text-slate-300">{label}</label>
            <input
                className="mt-2 w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-100 outline-none transition focus:border-cyan-500"
                value={value}
                onChange={(event) => onChange(event.target.value)}
                placeholder={placeholder}
            />
        </div>
    );
}

export function AiDetectionPage() {
    const [fraudForm, setFraudForm] = useState<FraudFormState>(
        fraudPresets.normal,
    );
    const [intrusionForm, setIntrusionForm] = useState<NetworkFormState>(
        networkPresets.attack,
    );
    const [autoencoderForm, setAutoencoderForm] = useState<NetworkFormState>(
        networkPresets.suspicious,
    );

    const [fraudResult, setFraudResult] = useState<DetectionResponse | null>(
        null,
    );
    const [intrusionResult, setIntrusionResult] =
        useState<DetectionResponse | null>(null);
    const [autoencoderResult, setAutoencoderResult] =
        useState<DetectionResponse | null>(null);

    const [fraudError, setFraudError] = useState<string | null>(null);
    const [intrusionError, setIntrusionError] = useState<string | null>(null);
    const [autoencoderError, setAutoencoderError] = useState<string | null>(null);

    const fraudMutation = useMutation({
        mutationFn: (payload: DetectionRequest) => runDetection("fraud", payload),
        onSuccess: (data) => setFraudResult(data),
        onError: (error) => setFraudError(getRequestErrorMessage(error)),
    });

    const intrusionMutation = useMutation({
        mutationFn: (payload: DetectionRequest) =>
            runDetection("intrusion", payload),
        onSuccess: (data) => setIntrusionResult(data),
        onError: (error) => setIntrusionError(getRequestErrorMessage(error)),
    });

    const autoencoderMutation = useMutation({
        mutationFn: (payload: DetectionRequest) =>
            runDetection("autoencoder", payload),
        onSuccess: (data) => setAutoencoderResult(data),
        onError: (error) => setAutoencoderError(getRequestErrorMessage(error)),
    });

    function runFraudDetection() {
        setFraudError(null);
        setFraudResult(null);

        try {
            fraudMutation.mutate(buildFraudPayload(fraudForm));
        } catch (error) {
            setFraudError(
                error instanceof Error
                    ? error.message
                    : "Invalid fraud detection input.",
            );
        }
    }

    function runNetworkDetection(
        module: DetectionModule,
        form: NetworkFormState,
    ) {
        if (module === "intrusion") {
            setIntrusionError(null);
            setIntrusionResult(null);

            try {
                intrusionMutation.mutate(buildNetworkPayload(form));
            } catch (error) {
                setIntrusionError(
                    error instanceof Error
                        ? error.message
                        : "Invalid intrusion detection input.",
                );
            }

            return;
        }

        setAutoencoderError(null);
        setAutoencoderResult(null);

        try {
            autoencoderMutation.mutate(buildNetworkPayload(form));
        } catch (error) {
            setAutoencoderError(
                error instanceof Error
                    ? error.message
                    : "Invalid autoencoder detection input.",
            );
        }
    }

    return (
        <div className="space-y-6">
            <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
                <div className="flex items-start gap-3">
                    <div className="rounded-xl border border-cyan-500/20 bg-cyan-500/10 p-3 text-cyan-300">
                        <BrainCircuit size={26} />
                    </div>

                    <div>
                        <h2 className="text-xl font-semibold">AI Detection Lab</h2>
                        <p className="mt-1 text-sm text-slate-400">
                            Run AI-assisted fraud, intrusion and anomaly checks using validated demo presets.
                        </p>
                    </div>
                </div>
            </div>

            <section className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
                <div className="flex items-start gap-3">
                    <div className="rounded-xl border border-emerald-500/20 bg-emerald-500/10 p-3 text-emerald-300">
                        <ShieldCheck size={22} />
                    </div>

                    <div>
                        <h3 className="text-lg font-semibold">Fraud Detection</h3>
                        <p className="mt-1 text-sm text-slate-400">
                            Simplified transaction form mapped to the 30-feature fraud detection model.
                        </p>
                    </div>
                </div>

                <div className="mt-5 flex flex-wrap gap-2">
                    {(["normal", "suspicious", "high-risk"] as FraudPreset[]).map(
                        (preset) => (
                            <button
                                key={preset}
                                onClick={() => {
                                    setFraudForm(fraudPresets[preset]);
                                    setFraudError(null);
                                    setFraudResult(null);
                                }}
                                className="rounded-lg border border-slate-700 px-3 py-2 text-xs font-semibold text-slate-300 transition hover:border-cyan-400 hover:text-cyan-200"
                                type="button"
                            >
                                {preset}
                            </button>
                        ),
                    )}
                </div>

                <div className="mt-5 grid gap-4 xl:grid-cols-2">
                    <div className="space-y-4">
                        <div className="grid gap-4 md:grid-cols-2">
                            <TextField
                                label="Amount"
                                value={fraudForm.amount}
                                onChange={(value) =>
                                    setFraudForm({ ...fraudForm, amount: value })
                                }
                            />

                            <TextField
                                label="Failed login attempts"
                                value={fraudForm.failedLogins}
                                onChange={(value) =>
                                    setFraudForm({
                                        ...fraudForm,
                                        failedLogins: value,
                                    })
                                }
                            />

                            <TextField
                                label="Account age days"
                                value={fraudForm.accountAgeDays}
                                onChange={(value) =>
                                    setFraudForm({
                                        ...fraudForm,
                                        accountAgeDays: value,
                                    })
                                }
                            />

                            <TextField
                                label="Transaction velocity"
                                value={fraudForm.transactionVelocity}
                                onChange={(value) =>
                                    setFraudForm({
                                        ...fraudForm,
                                        transactionVelocity: value,
                                    })
                                }
                            />
                        </div>

                        <label className="flex items-center gap-3 rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-300">
                            <input
                                checked={fraudForm.foreignTransaction}
                                onChange={(event) =>
                                    setFraudForm({
                                        ...fraudForm,
                                        foreignTransaction:
                                            event.target.checked,
                                    })
                                }
                                type="checkbox"
                            />
                            Foreign transaction
                        </label>

                        {fraudError && (
                            <div className="rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-300">
                                {fraudError}
                            </div>
                        )}

                        <button
                            onClick={runFraudDetection}
                            disabled={fraudMutation.isPending}
                            className="inline-flex items-center gap-2 rounded-lg bg-cyan-500 px-4 py-2 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-60"
                            type="button"
                        >
                            <ScanSearch size={16} />
                            {fraudMutation.isPending
                                ? "Analyzing..."
                                : "Run fraud detection"}
                        </button>
                    </div>

                    <ResultPanel
                        result={fraudResult}
                        isPending={fraudMutation.isPending}
                    />
                </div>
            </section>

            <NetworkDetectionSection
                title="Intrusion Detection"
                description="Detect suspicious network traffic and create security alerts from compact network input."
                icon="shield"
                form={intrusionForm}
                setForm={setIntrusionForm}
                presets={networkPresets}
                error={intrusionError}
                result={intrusionResult}
                isPending={intrusionMutation.isPending}
                onRun={() => runNetworkDetection("intrusion", intrusionForm)}
            />

            <NetworkDetectionSection
                title="Autoencoder Anomaly Detection"
                description="Detect network anomalies using the autoencoder model with simplified traffic input."
                icon="network"
                form={autoencoderForm}
                setForm={setAutoencoderForm}
                presets={networkPresets}
                error={autoencoderError}
                result={autoencoderResult}
                isPending={autoencoderMutation.isPending}
                onRun={() => runNetworkDetection("autoencoder", autoencoderForm)}
            />
        </div>
    );
}

type NetworkDetectionSectionProps = {
    title: string;
    description: string;
    icon: "shield" | "network";
    form: NetworkFormState;
    setForm: (form: NetworkFormState) => void;
    presets: Record<NetworkPreset, NetworkFormState>;
    error: string | null;
    result: DetectionResponse | null;
    isPending: boolean;
    onRun: () => void;
};

function NetworkDetectionSection({
    title,
    description,
    icon,
    form,
    setForm,
    presets,
    error,
    result,
    isPending,
    onRun,
}: NetworkDetectionSectionProps) {
    const Icon = icon === "shield" ? ShieldAlert : Network;

    return (
        <section className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
            <div className="flex items-start gap-3">
                <div className="rounded-xl border border-cyan-500/20 bg-cyan-500/10 p-3 text-cyan-300">
                    <Icon size={22} />
                </div>

                <div>
                    <h3 className="text-lg font-semibold">{title}</h3>
                    <p className="mt-1 text-sm text-slate-400">{description}</p>
                </div>
            </div>

            <div className="mt-5 flex flex-wrap gap-2">
                {(["normal", "suspicious", "attack"] as NetworkPreset[]).map(
                    (preset) => (
                        <button
                            key={preset}
                            onClick={() => setForm(presets[preset])}
                            className="rounded-lg border border-slate-700 px-3 py-2 text-xs font-semibold text-slate-300 transition hover:border-cyan-400 hover:text-cyan-200"
                            type="button"
                        >
                            {preset}
                        </button>
                    ),
                )}

                <button
                    onClick={() => setForm(presets.normal)}
                    className="inline-flex items-center gap-2 rounded-lg border border-slate-700 px-3 py-2 text-xs font-semibold text-slate-300 transition hover:border-cyan-400 hover:text-cyan-200"
                    type="button"
                >
                    <RotateCcw size={14} />
                    Reset
                </button>
            </div>

            <div className="mt-5 grid gap-4 xl:grid-cols-2">
                <div className="space-y-4">
                    <div className="grid gap-4 md:grid-cols-2">
                        <TextField
                            label="Source IP"
                            value={form.sourceIp}
                            onChange={(value) =>
                                setForm({ ...form, sourceIp: value })
                            }
                        />

                        <TextField
                            label="Destination IP"
                            value={form.destinationIp}
                            onChange={(value) =>
                                setForm({ ...form, destinationIp: value })
                            }
                        />

                        <TextField
                            label="Protocol"
                            value={form.protocol}
                            onChange={(value) =>
                                setForm({ ...form, protocol: value })
                            }
                            placeholder="tcp, udp, icmp"
                        />

                        <TextField
                            label="Duration"
                            value={form.duration}
                            onChange={(value) =>
                                setForm({ ...form, duration: value })
                            }
                        />

                        <TextField
                            label="Bytes sent"
                            value={form.bytesSent}
                            onChange={(value) =>
                                setForm({ ...form, bytesSent: value })
                            }
                        />

                        <TextField
                            label="Bytes received"
                            value={form.bytesReceived}
                            onChange={(value) =>
                                setForm({ ...form, bytesReceived: value })
                            }
                        />

                        <TextField
                            label="Packets sent"
                            value={form.packetsSent}
                            onChange={(value) =>
                                setForm({ ...form, packetsSent: value })
                            }
                        />

                        <TextField
                            label="Packets received"
                            value={form.packetsReceived}
                            onChange={(value) =>
                                setForm({ ...form, packetsReceived: value })
                            }
                        />
                    </div>

                    {error && (
                        <div className="rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-300">
                            {error}
                        </div>
                    )}

                    <button
                        onClick={onRun}
                        disabled={isPending}
                        className="inline-flex items-center gap-2 rounded-lg bg-cyan-500 px-4 py-2 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-60"
                        type="button"
                    >
                        <ScanSearch size={16} />
                        {isPending ? "Analyzing..." : "Run detection"}
                    </button>
                </div>

                <ResultPanel result={result} isPending={isPending} />
            </div>
        </section>
    );
}