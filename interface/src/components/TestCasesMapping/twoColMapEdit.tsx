import { useEffect } from "react";
import styles from "../../styles/columnRelationship.module.css";
import { mapRelationshipElements } from "../../constants/TestCasesMapping/mapRelationshipElements";
import { Subtitle, MiddleColumn, Row, Column } from "../../utils/formatUtils";
import { MainJsonKey } from "../../utils/formatUtils";
import { Button } from "@mui/material";
import { JsonNestedTreeEdit } from "./jsonNestedTreeEdit";

interface TwoColMapEditInterface {
  file?: String | null;
  setFile: (file: String | null) => void;
}

const TwoColMapEdit: React.FC<TwoColMapEditInterface> = ({ file, setFile }) => {

  const {
    error,
    fileData,
    jsonObjs,
    handleFileData,
    handleJsonChange,
    handleDeleteJson,
    handleAddJsonHere,
    onAlertDialogAddJsonHere,
    handleSaveFileData
  } = mapRelationshipElements({ setFile });

  useEffect(() => {
    if (file) {
      handleFileData(file);
    }
  }, [file]);

  return (
    <>
      <div className={styles.ColumnRelationship}>
        { fileData && (
          <Row mt={0} mb={0}>
            <Column>
              <Button
                className={`${styles.button} ${styles.buttonSave}`}
                style={{marginLeft: '10px', marginRight: '10px'}}
                onClick={handleSaveFileData}>Save File</Button>
              <Button
                className={`${styles.button} ${styles.buttonReload}`}
                style={{marginLeft: '10px', marginRight: '10px'}}
                onClick={() => handleFileData(file ? file : null)}>Reload File</Button>
            </Column>
          </Row>
        )}
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
                      <div className={styles.scrollableContainer}>
                        <MainJsonKey>{jsonKey}</MainJsonKey>
                        {Object.entries(jsonValue).map(([key, value]: [string, any], j: number) =>
                          <div key={`${i}-${j}`}>
                            <JsonNestedTreeEdit
                              jsonPath={[jsonKey]}
                              jsonKey={key}
                              jsonValue={value}
                              onSaveJson={handleJsonChange}
                              onDeleteJson={handleDeleteJson}
                              onAddJsonHere={handleAddJsonHere}
                              onAlertDialogAddJsonHere={onAlertDialogAddJsonHere}
                            />
                          </div>
                        )}
                      </div>
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

export default TwoColMapEdit;