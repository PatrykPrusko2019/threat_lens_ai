import { apiClient } from "./client";
import type {
    DetectionModule,
    DetectionRequest,
    DetectionResponse,
} from "../types/detection";

const endpointByModule: Record<DetectionModule, string> = {
    fraud: "/fraud/check",
    intrusion: "/intrusion/check",
    autoencoder: "/autoencoder/check",
};

export async function runDetection(
    module: DetectionModule,
    payload: DetectionRequest,
): Promise<DetectionResponse> {
    const response = await apiClient.post<DetectionResponse>(
        endpointByModule[module],
        payload,
    );

    return response.data;
}