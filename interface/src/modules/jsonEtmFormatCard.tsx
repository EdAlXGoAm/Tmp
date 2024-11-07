import React, {useState, useEffect} from 'react';
import { Row, Column, VariableText, VariableTextBorder, VariableArray, VariableArrayMinimalist } from '../utils/formatUtils';
import { jsonEtmFormatCardElements } from '../constants/jsonEtmFormatElement';
import { CodeContainer } from './codeContainer';
import TypeForm from './forms/typeForm';

interface JsonEtmFormatCardProps {
  jsonPath: Array<string>;
  jsonKey: string;
  jsonValue: any;
  onSaveJson: (jsonKey: string, jsonValue: any) => void;
}

export const JsonEtmFormatCard: React.FC<JsonEtmFormatCardProps> = ({ jsonPath, jsonKey, jsonValue, onSaveJson }) => {
  const {
    elementToEditType, setElementToEditType,
    isOpenExternalType, setIsOpenExternalType,
    onCleanData,
    handleEditType,
  } = jsonEtmFormatCardElements();

  return (
    <>
      <TypeForm
        onCleanData={onCleanData}
        elementToEdit={elementToEditType}
        isOpenExternal={isOpenExternalType}
        setIsOpenExternal={setIsOpenExternalType}
        updateType={() => null}
        createType={() => null}
      />
      <Row mt={1} mb={2}>
        <Column>
          <CodeContainer code={`${JSON.stringify(jsonValue, null, 2)}`} />
          {jsonValue && typeof jsonValue === 'object' && (
            <>
              {Object.entries(jsonValue).map(([key, value], i) => (
                <div key={i}>
                  {/* TYPE (string) */}
                  {key === 'type' && typeof value === 'string' ? (
                    <VariableText variable={'type'} value={value} onClick={() => handleEditType(key, value)}/>
                  ) : /* DEFAULT (string) */
                  key === 'default' && typeof value === 'string' ? (
                    <VariableTextBorder variable={key} value={value} color={'#f11f00'} onClick={() => null}/> // TODO: Add onClick
                  ) : /* STRING (string) */
                  typeof value === 'string' ? (
                    <VariableText variable={key} value={value} onClick={() => null}/> // TODO: Add onClick
                  ) : /* VALIDATION (object-array) */
                  key === 'validation' && typeof value === 'object' && Array.isArray(value) ? (
                    <VariableArrayMinimalist variable={key} value={value} onClick={() => null}/> // TODO: Add onClick
                  ) : /* ARRAY (object-array) */
                  typeof value === 'object' && Array.isArray(value) ? (
                    <VariableArray variable={key} value={value} color={'#f11f00'} onClick={() => null}/> // TODO: Add onClick
                  ) : null}
                </div>
              ))}
            </>
          )}
        </Column>
      </Row>
    </>
  );
}