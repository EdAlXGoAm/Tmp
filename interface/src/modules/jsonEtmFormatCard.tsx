import React, {useState, useEffect} from 'react';
import { Row, Column, VariableText, VariableTextBorder, VariableArray, VariableArrayMinimalist } from '../utils/formatUtils';
import { jsonEtmFormatCardElements } from '../constants/jsonEtmFormatElement';
import { CodeContainer } from './codeContainer';

interface JsonEtmFormatCardProps {
  jsonPath: Array<string>;
  jsonKey: string;
  jsonValue: any;
  onSaveJson: (jsonKey: string, jsonValue: any) => void;
}

export const JsonEtmFormatCard: React.FC<JsonEtmFormatCardProps> = ({ jsonPath, jsonKey, jsonValue, onSaveJson }) => {
  const {
    isNestedObject
  } = jsonEtmFormatCardElements();

  return (
    <Row mt={1} mb={2}>
      <Column>
        {/* <CodeContainer code={`${JSON.stringify(jsonValue, null, 2)}`} /> */}
        {jsonValue && typeof jsonValue === 'object' && (
          <>
            {Object.entries(jsonValue).map(([key, value], i) => (
              <div key={i}>
                {key === 'type' && typeof value === 'string' ? (
                  <VariableText variable={'type'} value={value}/> 
                ) : typeof value === 'string' ? (
                  <>
                    {key === 'default' ? (
                      <VariableTextBorder variable={key} value={value} color={'#f11f00'}/>
                    ) : (
                      <VariableText variable={key} value={value}/>
                    )}
                  </>
                ) : value && typeof value === 'object' && Array.isArray(value) ? (
                  <>
                    {key === 'validation' ? (
                      <VariableArrayMinimalist variable={key} value={value}/>
                    ) : (
                      <VariableArray variable={key} value={value} color={'#f11f00'}/>
                    )}
                  </>
                ) : (
                  <></>
                )}
              </div>
            ))}
          </>
        )}
      </Column>
    </Row>
  );
}