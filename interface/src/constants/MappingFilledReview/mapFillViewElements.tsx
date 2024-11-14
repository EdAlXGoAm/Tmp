import { useState } from "react";
import { invoke } from '@tauri-apps/api/core';

export const mapFillViewElements = () => {
  const [fileData, setFileData] = useState<any | null>(null);
  const [jsonTestCases, setJsonTestCases] = useState<any | null>(null);
  const [error, setError] = useState<String | null>(null);

  const handleFileData = async (file: String | null) => {
    try {
      const file_data = await invoke('read_file', { path: file });
      const json_data = JSON.parse(file_data as string);
      setFileData(file_data);
      setJsonTestCases(json_data);
    } catch (error) {
      setError("Error reading file");
    }
  };

  return {
    fileData, setFileData,
    jsonTestCases, setJsonTestCases,
    error, setError,
    handleFileData
  };
}
