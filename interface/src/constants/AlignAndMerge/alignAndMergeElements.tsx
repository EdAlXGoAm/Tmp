import { useState } from "react";
import { invoke } from "@tauri-apps/api/core";

export const alignAndMergeElements = () => {
  const [error, setError] = useState<string | null>(null);
  const [jsonObjsArray, setJsonObjsArray] = useState<any[]>([])
  const handleFileData = async (files: string[]) => {
    try {
      const jsonObjsArray: any[] = [];
      for (const file of files) {
        const file_data = await invoke<string>('read_file', { path: file });
        const json_data = JSON.parse(file_data);
        // keep only the first 2 objects from the json_data
        const json_data_cut = json_data.slice(0, 2);
        jsonObjsArray.push(json_data_cut);
      }
      setJsonObjsArray(jsonObjsArray);
    } catch (error) {
      setError("Error reading file");
    }
  }

  return {
    error, setError,
    jsonObjsArray, setJsonObjsArray,
    handleFileData
  }
}
