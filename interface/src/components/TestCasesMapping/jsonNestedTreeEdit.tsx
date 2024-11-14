import React, { useState } from 'react';
import { JsonKeyGroup, JsonKey } from '../../utils/formatUtils';
import { CustomDelete, CustomAddHere, CustomAngleRight, CustomAngleDown } from '../../utils/buttonUtils';
import { Row, Column, CardContainer } from '../../utils/formatUtils';
import { jsonCardNestedElements } from '../../constants/TestCasesMapping/jsonCardNestedElements';
import { ObjCardBody } from '../ComonObjComponetes/objCardBody';

interface JsonNestedTreeEditProps {
  jsonPath: Array<string>;
  jsonKey: string;
  jsonValue: any;
  onSaveJson: (jsonPath: Array<string>, jsonKey: string, jsonValue: any) => void;
  onDeleteJson: (jsonPath: Array<string>, jsonKey: string) => void;
  onAddJsonHere: (jsonPath: Array<string>, jsonKey: string, jsonValue: any, nextToKey: string) => void;
  onAlertDialogAddJsonHere?: () => string | null;
  indent?: number;
}

export const JsonNestedTreeEdit: React.FC<JsonNestedTreeEditProps> = ({ jsonPath, jsonKey, jsonValue, onSaveJson, onDeleteJson, onAddJsonHere, onAlertDialogAddJsonHere, indent = 0 }) => {
  const {
    isNestedObject
  } = jsonCardNestedElements();

  const [isVisible, setIsVisible] = useState(true);

  const handleToggleVisibility = () => {
    setIsVisible(!isVisible);
  };

  const paddingLeft = indent * 20;

  const [deleteable, setDeleteable] = useState(true);
  const [addable, setAddable] = useState(true);
  const handleDelete = () => {
    setDeleteable(false);
    onDeleteJson(jsonPath, jsonKey);
    setDeleteable(true);
  };
  const handleAdd = () => {
    setAddable(false);
    const newKey = onAlertDialogAddJsonHere ? onAlertDialogAddJsonHere() : null;
    if (newKey) {
      onAddJsonHere(jsonPath, newKey, jsonValue, jsonKey);
    }
    setAddable(true);
  };

  return (
    <Row mt={1} mb={2} style={{ paddingLeft }}>
      <Column>
        {isNestedObject(jsonValue) ? (
          <>
            <div onClick={handleToggleVisibility} style={{ cursor: 'pointer' }}>
              <JsonKeyGroup icon={!isVisible ? <CustomAngleRight/> : <CustomAngleDown/>}>{jsonKey}</JsonKeyGroup>
            </div>
            {isVisible && (
              <CardContainer>
                {Object.entries(jsonValue).map(([key, value], i) => (
                  <JsonNestedTreeEdit
                    key={`${jsonKey}-${key}-${i}`}
                    jsonPath={[...jsonPath, jsonKey]}
                    jsonKey={key}
                    jsonValue={value}
                    onSaveJson={onSaveJson}
                    onDeleteJson={onDeleteJson}
                    onAddJsonHere={onAddJsonHere}
                    onAlertDialogAddJsonHere={onAlertDialogAddJsonHere}
                    indent={indent + 1}
                  />
                ))}
              </CardContainer>
            )}
          </>
        ) : (
          <>
            <div>
              <JsonKey onClick={handleToggleVisibility} icon={!isVisible ? <CustomAngleRight/> : <CustomAngleDown/>}>{jsonKey}</JsonKey>
            </div>
            {isVisible && (
              <>
                <CardContainer>
                  <ObjCardBody jsonPath={jsonPath} jsonKey={jsonKey} jsonValue={jsonValue} onSaveJson={onSaveJson} />
                  <CustomDelete onClick={handleDelete} deleteable={deleteable} />
                </CardContainer>
                {onAlertDialogAddJsonHere && <CustomAddHere onClick={handleAdd} addable={addable} />}
              </>
            )}
          </>
        )}
      </Column>
    </Row>
  );
};
