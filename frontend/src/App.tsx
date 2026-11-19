import { useEffect, useRef, useState } from "react";
import { requestRecommendation, type Album } from "./api";
import "./App.css";

const MAX_DESCRIPTION = 500;
type Status = "idle" | "loading" | "success" | "error";

function validationMessage(value: string): string | null {
  const trimmed = value.trim();
  if (!trimmed) {
    return "Please describe what you want to hear (up to 500 characters).";
  }
  if (trimmed.length > MAX_DESCRIPTION) {
    return "Please keep your description to 500 characters or fewer.";
  }
  return null;
}

export default function App() {
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState<Status>("idle");
  const [album, setAlbum] = useState<Album | null>(null);
  const [errorMessage, setErrorMessage] = useState("");
  const resultHeadingRef = useRef<HTMLHeadingElement>(null);
  const errorHeadingRef = useRef<HTMLHeadingElement>(null);

  useEffect(() => {
    if (status === "success") {
      resultHeadingRef.current?.focus();
    } else if (status === "error") {
      errorHeadingRef.current?.focus();
    }
  }, [status]);

  async function submit(currentDescription: string) {
    const problem = validationMessage(currentDescription);
    if (problem) {
      setAlbum(null);
      setErrorMessage(problem);
      setStatus("error");
      return;
    }
    setStatus("loading");
    setErrorMessage("");
    try {
      const data = await requestRecommendation(currentDescription.trim(), []);
      setAlbum(data.album);
      setStatus("success");
    } catch {
      // Keep the description so the visitor can retry without retyping. P05.
      setAlbum(null);
      setErrorMessage(
        "Something went wrong. Your description is still here. Check your connection and try again."
      );
      setStatus("error");
    }
  }

  function onSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (status === "loading") {
      return;
    }
    void submit(description);
  }

  function onRetry() {
    if (status === "loading") {
      return;
    }
    void submit(description);
  }

  const loading = status === "loading";

  return (
    <main className="page">
      <h1>Jazzy Mood</h1>
      <p className="lede">
        Describe a mood and get one album from a small demo collection.
      </p>
      <p className="fixture-note">
        Demo data: the result comes from a tiny fixture, not the full
        catalogue.
      </p>

      <form onSubmit={onSubmit} noValidate>
        <label htmlFor="description">
          What do you want to hear? (up to 500 characters)
        </label>
        <textarea
          id="description"
          name="description"
          rows={4}
          maxLength={600}
          autoComplete="off"
          placeholder="Late-night jazz with a steady beat and no vocals."
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? "Finding an album…" : "Recommend an album"}
        </button>
      </form>

      <div aria-live="polite" className="status">
        {loading ? <p>Looking for one album. Please wait…</p> : null}
      </div>

      {status === "success" && album ? (
        <section aria-label="Recommended album" className="card">
          <h2 ref={resultHeadingRef} tabIndex={-1}>
            {album.artist} — {album.title}
          </h2>
          {album.year !== null ? <p>Released: {album.year}</p> : null}
          <p>{album.reason}</p>
          <p>
            <a href={album.listening_url} target="_blank" rel="noreferrer">
              {album.listening_label}: {album.artist} — {album.title}
            </a>
          </p>
        </section>
      ) : null}

      {status === "error" ? (
        <section aria-label="Request problem" className="card error">
          <h2 ref={errorHeadingRef} tabIndex={-1}>
            We could not finish that request
          </h2>
          <p role="alert">{errorMessage}</p>
          <button type="button" onClick={onRetry} disabled={loading}>
            Try again
          </button>
        </section>
      ) : null}
    </main>
  );
}
