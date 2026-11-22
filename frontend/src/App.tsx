import { useEffect, useRef, useState } from "react";
import { requestRecommendation, type Album } from "./api";
import "./App.css";

const MAX_DESCRIPTION = 500;
type Status = "idle" | "loading" | "success" | "error";
type ErrorKind = "validation" | "request" | null;

function codePointLength(value: string): number {
  // Match Python len(): count Unicode code points, not UTF-16 units.
  return Array.from(value).length;
}

function validationMessage(value: string): string | null {
  const trimmed = value.trim();
  if (!trimmed) {
    return "Please describe what you want to hear (up to 500 characters).";
  }
  if (codePointLength(trimmed) > MAX_DESCRIPTION) {
    return "Please keep your description to 500 characters or fewer.";
  }
  return null;
}

export default function App() {
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState<Status>("idle");
  const [errorKind, setErrorKind] = useState<ErrorKind>(null);
  const [album, setAlbum] = useState<Album | null>(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [requestId, setRequestId] = useState<string | null>(null);
  const resultHeadingRef = useRef<HTMLHeadingElement>(null);
  const errorHeadingRef = useRef<HTMLHeadingElement>(null);
  const descriptionRef = useRef<HTMLTextAreaElement>(null);
  // Synchronous guard: state updates flush after the handler, so two
  // clicks in one task would both read a stale `status`.
  const submittingRef = useRef(false);

  useEffect(() => {
    if (status === "success") {
      resultHeadingRef.current?.focus();
    } else if (status === "error") {
      // A validation problem is fixed in the field, so focus moves back
      // to the textarea. A failed request keeps the retry button path.
      if (errorKind === "validation") {
        descriptionRef.current?.focus();
      } else {
        errorHeadingRef.current?.focus();
      }
    }
  }, [status, errorKind]);

  async function submit(currentDescription: string) {
    const problem = validationMessage(currentDescription);
    if (problem) {
      setAlbum(null);
      setErrorKind("validation");
      setErrorMessage(problem);
      setRequestId(null);
      setStatus("error");
      return;
    }
    setStatus("loading");
    setErrorMessage("");
    setErrorKind(null);
    setRequestId(null);
    try {
      const result = await requestRecommendation(currentDescription.trim(), []);
      setAlbum(result.album);
      setErrorKind(null);
      setStatus("success");
    } catch (error) {
      // Keep the description so the visitor can retry without retyping. P05.
      setAlbum(null);
      const failure = error as { status?: number; requestId?: string | null };
      setRequestId(failure.requestId ?? null);
      if (failure.status === 422) {
        setErrorKind("validation");
        setErrorMessage(
          "The description was not accepted. Please keep it to 1–500 characters."
        );
      } else {
        setErrorKind("request");
        setErrorMessage(
          "Something went wrong. Your description is still here. Check your connection and try again."
        );
      }
      setStatus("error");
    }
  }

  function onSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (submittingRef.current) {
      return;
    }
    submittingRef.current = true;
    void submit(description).finally(() => {
      submittingRef.current = false;
    });
  }

  function onRetry() {
    if (submittingRef.current) {
      return;
    }
    submittingRef.current = true;
    void submit(description).finally(() => {
      submittingRef.current = false;
    });
  }

  const loading = status === "loading";
  const count = codePointLength(description);
  const describedBy =
    status === "error" && errorKind === "validation"
      ? "description-hint description-error"
      : "description-hint";

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
          ref={descriptionRef}
          rows={4}
          maxLength={500}
          autoComplete="off"
          placeholder="Late-night jazz with a steady beat and no vocals."
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          disabled={loading}
          aria-describedby={describedBy}
          aria-invalid={status === "error" && errorKind === "validation"}
        />
        <div className="field-meta">
          <p id="description-hint" className="hint">
            Up to 500 characters.
          </p>
          <p className="counter">
            {count} / {MAX_DESCRIPTION}
          </p>
        </div>
        {status === "error" && errorKind === "validation" ? (
          <>
            <p id="description-error" role="alert" className="inline-error">
              {errorMessage}
            </p>
            {requestId ? (
              <p className="reference">
                Reference {requestId} — include it if you report this problem.
              </p>
            ) : null}
          </>
        ) : null}
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
        </section>
      ) : null}

      {status === "error" && errorKind === "request" ? (
        <section aria-label="Request problem" className="card error">
          <h2 ref={errorHeadingRef} tabIndex={-1}>
            We could not finish that request
          </h2>
          <p role="alert">{errorMessage}</p>
          {requestId ? (
            <p className="reference">
              Reference {requestId} — include it if you report this problem.
            </p>
          ) : null}
          <button type="button" onClick={onRetry} disabled={loading}>
            Try again
          </button>
        </section>
      ) : null}
    </main>
  );
}
