export interface Album {
  id: string;
  artist: string;
  title: string;
  year: number | null;
  reason: string;
  tag_status: string;
}

export interface RecommendationResponse {
  album: Album;
  mode: string;
}

export class RecommendationError extends Error {
  status?: number;
  requestId: string | null = null;
}

export interface RecommendationResult {
  album: Album;
  mode: string;
  requestId: string | null;
}

export async function requestRecommendation(
  description: string,
  recentIds: string[] = []
): Promise<RecommendationResult> {
  let response: Response;
  try {
    response = await fetch("/api/recommendations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ description, recent_ids: recentIds })
    });
  } catch {
    throw new RecommendationError("Request failed before a response arrived.");
  }
  const requestId = response.headers.get("X-Request-ID");
  if (!response.ok) {
    const failure = new RecommendationError(
      `Request failed with status ${response.status}.`
    );
    failure.status = response.status;
    failure.requestId = requestId;
    throw failure;
  }
  const data = (await response.json()) as RecommendationResponse;
  return { album: data.album, mode: data.mode, requestId };
}
