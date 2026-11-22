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
  recentIds: string[] = [],
  timeoutMs = 15000
): Promise<RecommendationResult> {
  let response: Response;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    response = await fetch("/api/recommendations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ description, recent_ids: recentIds }),
      signal: controller.signal
    });
  } catch {
    throw new RecommendationError("Request failed before a response arrived.");
  } finally {
    clearTimeout(timer);
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
  let data: RecommendationResponse;
  try {
    data = (await response.json()) as RecommendationResponse;
  } catch {
    const failure = new RecommendationError("Request returned an unreadable response.");
    failure.requestId = requestId;
    throw failure;
  }
  return { album: data.album, mode: data.mode, requestId };
}
