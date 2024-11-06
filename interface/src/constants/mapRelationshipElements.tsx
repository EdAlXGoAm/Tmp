import { useState } from "react";
import { invoke } from '@tauri-apps/api/core';

export const mapRelationshipElements = () => {
  const [fileData, setFileData] = useState<any | null>(null);
  const [jsonObjs, setJsonObjs] = useState<any | null>(null);
  const [error, setError] = useState<String | null>(null);

  const handleFileData = async (file: String | null) => {
    try {
      if (!file) return;
      const file_data = await invoke('read_file', { path: file });
      const json_data = JSON.parse(file_data as string);
      setFileData(file_data);
      setJsonObjs(json_data);
    } catch (error) {
      setError("Error reading file");
      console.error(error);
    }
  };

  const handleJsonChange = (updatedKey: string, updatedValue: any) => {
    const updatedJsonObjs = { ...jsonObjs };

    if (updatedJsonObjs && updatedJsonObjs[updatedKey]) {
      updatedJsonObjs[updatedKey] = updatedValue;
      setJsonObjs(updatedJsonObjs);
    }
  };

  return {
    fileData, setFileData,
    jsonObjs, setJsonObjs,
    error, setError,
    handleFileData,
    handleJsonChange
  };
}