import { useState, useEffect } from "react";
import "../styles/columnRelationship.module.css";
import { Subtitle, MiddleColumn } from "../utils/formatUtils";
import { MainJsonKey } from "../utils/formatUtils";
import { mapRelationshipElements } from "../constants/mapRelationshipElements";
import { JsonCardNested } from "./jsonCardNested";

interface FileInterface {
  file?: String | null;
}

const MapRelationship: React.FC<FileInterface> = ({ file }) => {

  const {
    error, setError,
    fileData, setFileData,
    jsonObjs, setJsonObjs,
    handleFileData,
    handleJsonChange
  } = mapRelationshipElements();

  useEffect(() => {
    let intervalId: ReturnType<typeof setInterval> | undefined;
  
    if (file) {
      handleFileData(file);
      intervalId = setInterval(() => {
        handleFileData(file);
      }, 5000);
    }
  
    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [file]);

  return (
    <>
      <div className="ColumnRelationship">
        <Subtitle>Relationships</Subtitle>
        {fileData ? (
          <div>
            <Subtitle mt={0}>File Data</Subtitle>
            {error && <p>{error}</p>}
            {jsonObjs && typeof jsonObjs === 'object' && (
              <>
                <Subtitle mt={0}>JSON Objects</Subtitle>
                <div className="row">
                  {Object.entries(jsonObjs).slice(-2).map(([jsonKey, jsonValue]: [string, any], i: number) => (
                    <MiddleColumn key={i}>
                      <MainJsonKey>{jsonKey}</MainJsonKey>
                      {Object.entries(jsonValue).map(([key, value]: [string, any], j: number) =>
                        <div key={`${i}-${j}`}>
                          <JsonCardNested
                            jsonPath={[jsonKey]}
                            jsonKey={key}
                            jsonValue={value}
                            onSaveJson={handleJsonChange}
                          />
                        </div>
                      )}
                    </MiddleColumn>
                  ))}
                </div>
              </>
            )}
          </div>
        ) : (
          <>
            <p>No data</p>
            <p>{error}</p>
          </>
        )}
      </div>
    </>
  )
}

export default MapRelationship;