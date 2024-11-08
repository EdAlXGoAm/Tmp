import React, { useState } from 'react';
import { JsonKeyGroup, JsonKey, JsonValue, CustomDelete, CustomAddHere } from '../utils/formatUtils';
import { Row, Column, CardContainer } from '../utils/formatUtils';
import { jsonCardNestedElements } from '../constants/jsonCardNestedElements';
import { MapCardBody } from './mapCardBody';
import { CustomAngleRight, CustomAngleDown } from '../utils/formatUtils';

interface JsonCardProps {
  jsonPath: Array<string>;
  jsonKey: string;
  jsonValue: any;
  onSaveJson: (jsonPath: Array<string>, jsonKey: string, jsonValue: any) => void;
  onDeleteJson: (jsonPath: Array<string>, jsonKey: string) => void;
  onAddJsonHere: (jsonPath: Array<string>, jsonKey: string, jsonValue: any, nextToKey: string) => void;
  onAlertDialogAddJsonHere: () => string | null;
  indent?: number;
}

export const JsonCardNested: React.FC<JsonCardProps> = ({ jsonPath, jsonKey, jsonValue, onSaveJson, onDeleteJson, onAddJsonHere, onAlertDialogAddJsonHere, indent = 0 }) => {
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
    const newKey = onAlertDialogAddJsonHere();
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
                  <JsonCardNested
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
            <div onClick={handleToggleVisibility} style={{ cursor: 'pointer' }}>
              <JsonKey icon={!isVisible ? <CustomAngleRight/> : <CustomAngleDown/>}>{jsonKey}</JsonKey>
            </div>
            {isVisible && (
              <>
                <CardContainer>
                  <MapCardBody jsonPath={jsonPath} jsonKey={jsonKey} jsonValue={jsonValue} onSaveJson={onSaveJson} />
                  <CustomDelete onClick={handleDelete} deleteable={deleteable} />
                </CardContainer>
                <CustomAddHere onClick={handleAdd} addable={addable} />
              </>
            )}
          </>
        )}
      </Column>
    </Row>
  );
};
