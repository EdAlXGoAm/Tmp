import React, { useEffect, useState } from 'react';
import { JsonKeyGroup, JsonKey } from '../../utils/formatUtils';
import { CustomAngleRight, CustomAngleDown } from '../../utils/buttonUtils';
import { Row, Column, CardContainer } from '../../utils/formatUtils';
import { jsonCardNestedElements } from '../../constants/TestCasesMapping/jsonCardNestedElements';
import { ObjCardBody } from '../ComonObjComponetes/objCardBody';

interface JsonNestedTreeViewProps {
  jsonPath: Array<string>;
  jsonKey: string;
  jsonValue: any;
  indent?: number;
  forceInvisibility?: boolean;
  setForceInvisibility?: (forceInvisibility: boolean) => void;
  forceVisibility?: boolean;
  setForceVisibility?: (forceVisibility: boolean) => void;
}

export const JsonNestedTreeView: React.FC<JsonNestedTreeViewProps> = ({ 
  jsonPath,
  jsonKey,
  jsonValue,
  indent = 0,
  forceInvisibility = false,
  setForceInvisibility = () => {},
  forceVisibility = false,
  setForceVisibility = () => {}
}) => {
  const {
    isNestedObject
  } = jsonCardNestedElements();

  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    if (forceVisibility) {
      setIsVisible(true);
      setForceVisibility && setForceVisibility(false);
    }
    if (forceInvisibility) {
      setIsVisible(false);
      setForceInvisibility && setForceInvisibility(false);
    }
  }, [forceVisibility, forceInvisibility]);

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
                  <JsonNestedTreeView
                    key={`${jsonKey}-${key}-${i}`}
                    jsonPath={[...jsonPath, jsonKey]}
                    jsonKey={key}
                    jsonValue={value}
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
                  <ObjCardBody jsonPath={jsonPath} jsonKey={jsonKey} jsonValue={jsonValue} />
              </>
            )}
          </>
        )}
      </Column>
    </Row>
  );
};
