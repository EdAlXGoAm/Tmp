import { useState } from "react";
import { invoke } from '@tauri-apps/api/core';
import { mapCardBodyElements } from '../constants/mapCardBodyElements';

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

  const handleJsonChange = (jsonPath: Array<string>, updatedKey: string, updatedValue: any) => {
    setJsonObjs((prevJsonObjs: any) => {
      const newJson = { ...prevJsonObjs };

      let current = newJson;
      for (let i = 0; i < jsonPath.length; i++) {
        const key = jsonPath[i];
          
        if (!(key in current)) {
          current[key] = {};
        } else if (typeof current[key] !== 'object' || current[key] === null) {
          throw new Error(`La ruta ${jsonPath.slice(0, i + 1).join('.')} no es un objeto válido.`);
        }
          
        current[key] = { ...current[key] };
        current = current[key];
      }

      current[updatedKey] = updatedValue;

      return newJson;
    });
  };

  const handleDeleteJson = (jsonPath: Array<string>, jsonKey: string) => {
    setJsonObjs((prevJsonObjs: any) => {
      const newJson = { ...prevJsonObjs };
      let current = newJson;
      for (let i = 0; i < jsonPath.length; i++) {
        const key = jsonPath[i];

        if (!(key in current)) {
          current[key] = {};
        } else if (typeof current[key] !== 'object' || current[key] === null) {
          throw new Error(`La ruta ${jsonPath.slice(0, i + 1).join('.')} no es un objeto válido.`);
        } 

        current[key] = { ...current[key] };
        current = current[key];
      }

      delete current[jsonKey];

      return newJson;
    });
  };

  const handleAddJsonHere = (jsonPath: Array<string>, jsonKey: string, jsonValue: any, nextToKey: string,) => {
    console.log('jsonValue', jsonValue);
    const {
      keysForTitleEvaluation,
      handleTypeEvaluation
    } = mapCardBodyElements();
    const typeEvaluation = handleTypeEvaluation(jsonValue, keysForTitleEvaluation, 'Title');
    console.log('typeEvaluation', typeEvaluation);
    let emptyJsonTestCaseFormat = {};
    if (typeEvaluation === 'Title') {
      emptyJsonTestCaseFormat = {
        "type" : "string",
        "content" : ""
      };
    }
    else {
      emptyJsonTestCaseFormat = {
        "type" : "string",
        "validation" : "",
        "default" : "",
        "content" : []
      };
    }
    handleJsonChange(jsonPath, jsonKey, emptyJsonTestCaseFormat);
    handleOrderJson(jsonPath, jsonKey, nextToKey);
  };

  const handleOrderJson = (jsonPath: Array<string>, jsonKey: string, nextToKey: string) => {
    setJsonObjs((prevJsonObjs: any) => {
      const copyAndReorder = (obj: any, path: Array<string>): any => {
        const key = path[0];
        if (path.length === 1) {
          const currentLevelObj = { ...obj[key] };
  
          const keys = Object.keys(currentLevelObj);
          const indexOfJsonKey = keys.indexOf(jsonKey);
          if (indexOfJsonKey === -1) {
            return obj;
          }
          keys.splice(indexOfJsonKey, 1);
  
          const indexOfNextToKey = keys.indexOf(nextToKey);
          if (indexOfNextToKey === -1) {
            return obj;
          }
          keys.splice(indexOfNextToKey + 1, 0, jsonKey);
  
          const reorderedObj: any = {};
          for (const k of keys) {
            reorderedObj[k] = currentLevelObj[k];
          }
  
          reorderedObj[jsonKey] = currentLevelObj[jsonKey];
  
          return { ...obj, [key]: reorderedObj };
        } else {
          return { ...obj, [key]: copyAndReorder(obj[key], path.slice(1)) };
        }
      };
  
      const updatedJson = copyAndReorder(prevJsonObjs, jsonPath);
      return updatedJson;
    });
  };

  const onAlertDialogAddJsonHere = () => {
    const newKey = window.prompt('Enter the new key:');
    return newKey;
  };

  const handleSaveFileData = (file: String | null) => {
    try {
      if (!file) return;
      invoke('write_file', { path: file, data: JSON.stringify(jsonObjs, null, 2) });
      handleFileData(file);
    } catch (error) {
      setError("Error writing file");
      console.error(error);
    }
  };

  return {
    fileData, setFileData,
    jsonObjs, setJsonObjs,
    error, setError,
    handleFileData,
    handleJsonChange,
    handleDeleteJson,
    handleAddJsonHere,
    onAlertDialogAddJsonHere,
    handleSaveFileData
  };
}