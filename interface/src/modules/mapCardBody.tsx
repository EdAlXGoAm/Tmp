import React, {useState, useEffect} from 'react';
import { Row, Column, CardContainer } from '../utils/formatUtils';
import { mapCardBodyElements } from '../constants/mapCardBodyElements';
import { JsonTitleCard } from './jsonTitleCard';
import { JsonEtmFormatCard } from './jsonEtmFormatCard';

interface mapCardBodyProps {
  jsonPath: Array<string>;
  jsonKey: string;
  jsonValue: any;
  onSaveJson: (jsonKey: string, jsonValue: any) => void;
}

export const MapCardBody: React.FC<mapCardBodyProps> = ({ jsonPath, jsonKey, jsonValue, onSaveJson }) => {
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
              <JsonTitleCard jsonPath={[...jsonPath, jsonKey]} jsonKey={jsonKey} jsonValue={jsonValue} onSaveJson={onSaveJson} />
            </>
          ) :
          handleTypeEvaluation(jsonValue, keysForEtmFormat, 'EtmFormat') === 'EtmFormat' ? (
            <>
              <JsonEtmFormatCard jsonPath={[...jsonPath, jsonKey]} jsonKey={jsonKey} jsonValue={jsonValue} onSaveJson={onSaveJson}/>
            </>
          ) : (
          <>I'm a unkown JSON</>
          )
        }
      </Column>
    </Row>
  )

;}