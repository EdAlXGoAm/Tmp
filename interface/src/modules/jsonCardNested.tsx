import React, { useState } from 'react';
import { JsonKeyGroup, JsonKey, JsonValue } from '../utils/formatUtils';
import { Row, Column, CardContainer } from '../utils/formatUtils';
import { jsonCardNestedElements } from '../constants/jsonCardNestedElements';
import { MapCardBody } from './mapCardBody';
import { CustomAngleRight, CustomAngleDown } from '../utils/formatUtils';

interface JsonCardProps {
  jsonPath: Array<string>;
  jsonKey: string;
  jsonValue: any;
  onSaveJson: (jsonKey: string, jsonValue: any) => void;
  indent?: number;
}

export const JsonCardNested: React.FC<JsonCardProps> = ({ jsonPath, jsonKey, jsonValue, onSaveJson, indent = 0 }) => {
  const {
    isNestedObject
  } = jsonCardNestedElements();

  const [isVisible, setIsVisible] = useState(true);

  const handleToggleVisibility = () => {
    setIsVisible(!isVisible);
  };

  const paddingLeft = indent * 20;

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
              <CardContainer>
                <MapCardBody jsonPath={jsonPath} jsonKey={jsonKey} jsonValue={jsonValue} onSaveJson={onSaveJson} />
              </CardContainer>
            )}
          </>
        )}
      </Column>
    </Row>
  );
};
