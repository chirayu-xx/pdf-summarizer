"use client";
import React, { ChangeEvent, useEffect, useState } from "react";
import { toast } from 'react-hot-toast';
type Props = {};

function FileUpload({}: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [text, setText] = useState("");

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  
  const uploadFile = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
  
    if (!file) {
      return;
    }
  
    const formData = new FormData();
    formData.append("file", file as File);
  
    try {
      await toast.promise(
        fetch("https://9a45-34-74-148-58.ngrok-free.app/summarize", {
          method: "POST",
          body: formData,
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("File upload failed.");
            }
            return response.json();
          })
          .then((data) => {
            const cleanedText = data.summary.replace(/[^a-zA-Z0-9\s\-:.]/g, "");
            setText(cleanedText);
          }),
        {
          loading: "Uploading and Summarizing",
          success: "Summarized successfully",
          error: "An error occurred during file upload",
        }
      );
    } catch (error) {
      console.error("An error occurred during file upload:", error);
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="flex flex-col gap-10 justify-center items-center">
      <form>
        <input type="file" accept=".pdf" onChange={handleFileChange} />
        <button disabled = {loading} onClick={uploadFile} className="bg-zinc-600 hover:bg-zinc-400 p-3 rounded-md">
          Summarize
        </button>
      </form>

      <p className="font-semibold text-lg max-w-3xl">{text}</p>
    </div>
  );
}

export default FileUpload;
