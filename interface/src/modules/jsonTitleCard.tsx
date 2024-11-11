import React from 'react';
import { Row, Column, VariableText, MiniTitle } from '../utils/formatUtils';
import { jsonTitleCardElements } from '../constants/jsonTitleCardElements';
import { CodeContainer } from './codeContainer';
import TypeForm from './forms/typeForm';

interface JsonTitleCardProps {
  jsonPath: Array<string>;
  jsonKey: string;
  jsonValue: any;
  onSaveJson: (jsonPath: Array<string>, jsonKey: string, jsonValue: any) => void;
}

export const JsonTitleCard: React.FC<JsonTitleCardProps> = ({ jsonPath, jsonKey, jsonValue, onSaveJson }) => {
  const {
    elementToEditType,
    isOpenExternalType, setIsOpenExternalType,
    onCleanDataType,
    onEditType,
    onUpdateType
  } = jsonTitleCardElements({ jsonPath, jsonKey, jsonValue, onSaveJson });

  return (
    <>
      <TypeForm
        onCleanData={onCleanDataType}
        elementToEdit={elementToEditType}
        isOpenExternal={isOpenExternalType}
        setIsOpenExternal={setIsOpenExternalType}
        updateType={onUpdateType}
        createType={() => null}
      />  
      <Row mt={1} mb={2}>
        <Column>
          {/* <CodeContainer code={`${JSON.stringify(jsonValue, null, 2)}`} /> */}
          {jsonValue && typeof jsonValue === 'object' && (
            <>
              {Object.entries(jsonValue).map(([key, value], i) => (
                <div key={i}>
                  {key === 'type' && typeof value === 'string' && (
                    <VariableText variable={'type'} value={value} onClick={() => onEditType(key, value)}/> 
                  )}
                </div>
              ))}
              <MiniTitle title={'Path'}/>
              <CodeContainer code={`${JSON.stringify([...jsonPath, jsonKey])}`} />
            </>
          )}
        </Column>
      </Row>
    </>
  );
}