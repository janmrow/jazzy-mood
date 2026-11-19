export interface Album {
  id: string;
  artist: string;
  title: string;
  year: number | null;
  listening_url: string;
  listening_label: string;
  reason: string;
  tag_status: string;
}

export interface RecommendationResponse {
  album: Album;
  mode: string;
}

export async function requestRecommendation(
  description: string,
  recentIds: string[] = []
): Promise<RecommendationResponse> {
  const response = await fetch("/api/recommendations", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ description, recent_ids: recentIds })
  });
  if (!response.ok) {
    const error = new Error(`Request failed with status ${response.status}.`);
    (error as { status?: number }).status = response.status;
    throw error;
  }
  return (await response.json()) as RecommendationResponse;
}
