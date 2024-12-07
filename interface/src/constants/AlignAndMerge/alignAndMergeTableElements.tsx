import { useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { save } from '@tauri-apps/plugin-dialog';

interface AlignAndMergeTableElementsProps {
  jsonObjsArray: any[];
}

export const alignAndMergeTableElements = ({ jsonObjsArray }: AlignAndMergeTableElementsProps) => {
  const [jsonKeys, setJsonKeys] = useState<string[]>([]);
  const [jsonKeysActions, setJsonKeysActions] = useState<any[]>([]);
  const [mergeContent, setMergeContent] = useState<any[]>([]);

  const crearObjetoVacio = (obj: any): any => {
    const objetoVacio: any = Array.isArray(obj) ? [] : {};
    
    for (const clave in obj) {
      if (typeof obj[clave] === 'object' && obj[clave] !== null) {
        objetoVacio[clave] = crearObjetoVacio(obj[clave]);
      } else {
        objetoVacio[clave] = typeof obj[clave] === 'string' ? '' : null;
      }
    }
    
    return objetoVacio;
  };

  const saveMergedFile = async (mergedByTestCases: any[]) => {
    const selectedPath = await save({
      filters: [{ name: 'JSON Files', extensions: ['json'] }],
      defaultPath: 'D:/edalxgoam/Tmp/MAPP/TestCasesMerged.json'
    });
    const mergedFile = JSON.stringify(mergedByTestCases, null, 2);
    invoke('write_file', { path: selectedPath as string, data: mergedFile });
  }

  const onSaveMergedFile = () => {
    if (jsonObjsArray.length > 0 && jsonObjsArray[0].length > 0) {
      let mergedByTestCases: any[] = [];
      for (let indexTestCase = 0; indexTestCase < jsonObjsArray[0].length; indexTestCase++) {
        const objetoVacio = crearObjetoVacio(jsonObjsArray[0][0]);
        jsonKeys.forEach((key, index) => {
          const keys = key.split('.');
          let referencia = objetoVacio;
  
          keys.forEach((k, i) => {
            if (i === keys.length - 1) {
              referencia[k] = mergeContent[indexTestCase][index];
            } else {
              referencia = referencia[k];
            }
          });
        });
        mergedByTestCases.push(objetoVacio);
      }
      // Open dialog to select path
      saveMergedFile(mergedByTestCases);
    }
  };

  const fetchJsonKeys = async (jsonObj: any) => {
    const numFiles = jsonObj.length;
    if (numFiles > 0) {
      let keys: string[] = [];
      let actionsTrue: boolean[] = [];
      let actionsFalse: boolean[] = [];

      for (const key in jsonObj[0][0]) {
        const procesarClave = (clave: string, subClave?: string) => {
          const claveCompuesta = subClave ? `${clave}.${subClave}` : clave;
          keys.push(claveCompuesta);
          actionsTrue.push(true);
          actionsFalse.push(false);
        };
      
        if (typeof jsonObj[0][0][key] !== 'object' || Array.isArray(jsonObj[0][0][key])) {
          procesarClave(key);
        } else {
          Object.keys(jsonObj[0][0][key]).forEach(subKey => procesarClave(key, subKey));
        }
      }
      setJsonKeys(keys);
      const actionsArray = Array.from({ length: numFiles }, (_, i) => (i === 0 ? actionsTrue : actionsFalse));
      setJsonKeysActions(actionsArray);

      let mergeContentArray: any[] = [];
      for (const i in jsonObj[0]) {
        let mergeContentArrayInKeysOfFirstFile: any[] = [];
        for (const key in jsonObj[0][i]) {
          const getMergeContent = (clave: string, subClave?: string) => {
            const valor = subClave ? jsonObj[0][i][clave][subClave] : jsonObj[0][i][clave];
            const contenido = typeof valor === 'string' 
              ? valor 
              : (Array.isArray(valor) && valor.length > 0 
                  ? valor
                  : '');
            mergeContentArrayInKeysOfFirstFile.push(contenido);
          };
        
          if (typeof jsonObj[0][i][key] !== 'object' || Array.isArray(jsonObj[0][i][key])) {
            getMergeContent(key);
          } else {
            Object.keys(jsonObj[0][i][key]).forEach(subKey => getMergeContent(key, subKey));
          }
        }
        mergeContentArray.push(mergeContentArrayInKeysOfFirstFile);
      }
      setMergeContent(mergeContentArray);
    }
  }

  return {
    jsonKeys, setJsonKeys,
    jsonKeysActions, setJsonKeysActions,
    mergeContent, setMergeContent,
    crearObjetoVacio,
    saveMergedFile,
    onSaveMergedFile,
    fetchJsonKeys
  }
}
