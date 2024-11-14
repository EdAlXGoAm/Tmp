import React from 'react';
import { Row, Column } from '../../utils/formatUtils';
import { mapCardBodyElements } from '../../constants/TestCasesMapping/mapCardBodyElements';
import { ObjTitleCard } from './objTitleCard';
import { ObjEtmFormatCard } from './objEtmFormatCard';
import { CodeContainer } from '../codeContainer';

interface ObjCardBodyProps {
  jsonPath: Array<string>;
  jsonKey: string;
  jsonValue: any;
  onSaveJson?: (jsonPath: Array<string>, jsonKey: string, jsonValue: any) => void;
}

const removeQuotes = (str: string) => {
  return str.replace(/^"|"$/g, '');
}

const lineBreak = (str: string) => {
  return str.replace(/\\n/g, '\n');
}

export const ObjCardBody: React.FC<ObjCardBodyProps> = ({ jsonPath, jsonKey, jsonValue, onSaveJson }) => {
  const {
    keysForTitleEvaluation,
    keysForEtmFormat,
    handleTypeEvaluation
  } = mapCardBodyElements();

  return (
    <Row mt={1} mb={2}>
      <Column>
        {jsonValue && typeof jsonValue === 'object' && 
          handleTypeEvaluation(jsonValue, keysForTitleEvaluation, 'Title') === 'Title' ? (
            <>
              {onSaveJson ? (
                <ObjTitleCard jsonPath={jsonPath} jsonKey={jsonKey} jsonValue={jsonValue} onSaveJson={onSaveJson} />
              ) : (
                <>
                  {Object.entries(jsonValue).map(([key, value], i) => (
                    <div key={i}>
                      {key==="content" && (
                        <CodeContainer code={`${lineBreak(removeQuotes(JSON.stringify(value, null, 2)))}`} expandable={true}/>
                      )}
                    </div>
                  ))}
                </>
              )}
            </>
          ) :
          handleTypeEvaluation(jsonValue, keysForEtmFormat, 'EtmFormat') === 'EtmFormat' ? (
            <>
              {onSaveJson ? (
                <ObjEtmFormatCard jsonPath={jsonPath} jsonKey={jsonKey} jsonValue={jsonValue} onSaveJson={onSaveJson}/>
              ) : (
                <>
                  {Object.entries(jsonValue).map(([key, value], i) => (
                    <div key={i}>
                      {key==="content" && (
                        <CodeContainer code={`${lineBreak(removeQuotes(JSON.stringify(value, null, 2)))}`} expandable={true}/>
                      )}
                    </div>
                  ))}
                </>
              )}
            </>
          ) : (
          <>I'm a unkown JSON</>
          )
        }
      </Column>
    </Row>
  )

;}