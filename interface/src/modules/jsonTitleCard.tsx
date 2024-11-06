import React, {useState, useEffect} from 'react';
import { Row, Column, VariableText, MiniTitle } from '../utils/formatUtils';
import { jsonTitleCardElements } from '../constants/jsonTitleCardElements';
import { CodeContainer } from './codeContainer';

interface JsonTitleCardProps {
  jsonPath: Array<string>;
  jsonKey: string;
  jsonValue: any;
  onSaveJson: (jsonKey: string, jsonValue: any) => void;
}

export const JsonTitleCard: React.FC<JsonTitleCardProps> = ({ jsonPath, jsonKey, jsonValue, onSaveJson }) => {
  const {
    isNestedObject
  } = jsonTitleCardElements();

  return (
    <Row mt={1} mb={2}>
      <Column>
        {jsonValue && typeof jsonValue === 'object' && (
          <>
            {Object.entries(jsonValue).map(([key, value], i) => (
              <div key={i}>
                {key === 'type' && typeof value === 'string' && (
                  <VariableText variable={'type'} value={value}/> 
                )}
              </div>
            ))}
            <MiniTitle title={'Path'}/>
            <CodeContainer code={`${JSON.stringify(jsonPath)}`} />
          </>
        )}
      </Column>
    </Row>
  );
}