import { useMutation } from "@tanstack/react-query";
import {
    BrainCircuit,
    ScanSearch,
    ShieldAlert,
    ShieldCheck,
} from "lucide-react";
import { useState } from "react";
import type { ElementType } from "react";

import { runDetection } from "../api/detectionApi";
import type {
    DetectionModule,
    DetectionRequest,
    DetectionResponse,
} from "../types/detection";

type DetectionCardProps = {
    module: DetectionModule;
    title: string;
    description: string;
    examplePayload: DetectionRequest;
    icon: ElementType;
};

function formatJson(value: unknown) {
    return JSON.stringify(value, null, 2);
}

function DetectionCard({
    module,
    title,
    description,
    examplePayload,
    icon: Icon,
}: DetectionCardProps) {
    const [payloadText, setPayloadText] = useState(formatJson(examplePayload));
    const [jsonError, setJsonError] = useState<string | null>(null);
    const [result, setResult] = useState<DetectionResponse | null>(null);

    const mutation = useMutation({
        mutationFn: (payload: DetectionRequest) => runDetection(module, payload),
        onSuccess: (data) => {
            setResult(data);
        },
    });

    function handleSubmit() {
        setJsonError(null);
        setResult(null);

        try {
            const parsedPayload = JSON.parse(payloadText) as DetectionRequest;
            mutation.mutate(parsedPayload);
        } catch {
            setJsonError("Invalid JSON payload.");
        }
    }

    function handleReset() {
        setPayloadText(formatJson(examplePayload));
        setJsonError(null);
        setResult(null);
    }

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

            <div className="mt-5 grid gap-4 xl:grid-cols-2">
                <div>
                    <div className="mb-2 flex items-center justify-between">
                        <label className="text-sm font-medium text-slate-300">
                            Request payload
                        </label>

                        <button
                            onClick={handleReset}
                            className="text-xs text-slate-500 transition hover:text-cyan-300"
                            type="button"
                        >
                            Reset example
                        </button>
                    </div>

                    <textarea
                        className="min-h-64 w-full rounded-xl border border-slate-800 bg-slate-950 p-4 font-mono text-xs text-slate-200 outline-none transition focus:border-cyan-500"
                        value={payloadText}
                        onChange={(event) => setPayloadText(event.target.value)}
                        spellCheck={false}
                    />

                    {jsonError && (
                        <p className="mt-2 text-sm text-red-300">{jsonError}</p>
                    )}

                    {mutation.isError && (
                        <p className="mt-2 text-sm text-red-300">
                            Detection request failed. Check backend logs and request payload.
                        </p>
                    )}

                    <button
                        onClick={handleSubmit}
                        disabled={mutation.isPending}
                        className="mt-4 inline-flex items-center gap-2 rounded-lg bg-cyan-500 px-4 py-2 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-60"
                        type="button"
                    >
                        <ScanSearch size={16} />
                        {mutation.isPending ? "Analyzing..." : "Run detection"}
                    </button>
                </div>

                <div>
                    <p className="mb-2 text-sm font-medium text-slate-300">
                        Detection result
                    </p>

                    <div className="min-h-64 rounded-xl border border-slate-800 bg-slate-950 p-4">
                        {!result && !mutation.isPending && (
                            <p className="text-sm text-slate-500">
                                Submit payload to see the backend detection response.
                            </p>
                        )}

                        {mutation.isPending && (
                            <p className="text-sm text-cyan-300">
                                Running detection module...
                            </p>
                        )}

                        {result && (
                            <pre className="overflow-auto whitespace-pre-wrap text-xs text-slate-200">
                                {formatJson(result)}
                            </pre>
                        )}
                    </div>
                </div>
            </div>
        </section>
    );
}

export function AiDetectionPage() {
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
                            Run fraud detection, intrusion detection and autoencoder anomaly
                            checks directly from the React dashboard.
                        </p>
                    </div>
                </div>
            </div>

            <DetectionCard
                module="fraud"
                title="Fraud Detection"
                description="Submit 30 numeric transaction features and receive backend fraud risk analysis."
                icon={ShieldCheck}
                examplePayload={{
                    features: [
                        1200,
                        5,
                        180,
                        1,
                        0,
                        0.25,
                        340,
                        12,
                        4,
                        0,
                        1,
                        0,
                        0.8,
                        0.1,
                        0.05,
                        2,
                        15,
                        3,
                        0,
                        1,
                        5000,
                        120,
                        30,
                        0.3,
                        0.7,
                        1,
                        0,
                        4,
                        9,
                        0.12,
                    ],
                }}
            />

            <DetectionCard
                module="intrusion"
                title="Intrusion Detection"
                description="Submit network traffic data and check whether activity looks suspicious."
                icon={ShieldAlert}
                examplePayload={{
                    source_ip: "192.168.1.10",
                    destination_ip: "10.0.0.5",
                    protocol: "tcp",
                    duration: 1.5,
                    bytes_sent: 6000000,
                    bytes_received: 80,
                    packets_sent: 60000,
                    packets_received: 20,
                }}
            />

            <DetectionCard
                module="autoencoder"
                title="Autoencoder Anomaly Detection"
                description="Submit network traffic data and receive anomaly detection output from the autoencoder module."
                icon={BrainCircuit}
                examplePayload={{
                    source_ip: "192.168.1.20",
                    destination_ip: "10.0.0.8",
                    protocol: "tcp",
                    duration: 3.2,
                    bytes_sent: 250000,
                    bytes_received: 1200,
                    packets_sent: 5000,
                    packets_received: 300,
                }}
            />
        </div>
    );
}