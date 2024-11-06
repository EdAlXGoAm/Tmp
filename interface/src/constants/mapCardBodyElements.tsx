import React, {useState, useEffect} from 'react';
import { Row, Column, CardContainer } from '../utils/formatUtils';

export const mapCardBodyElements = () => {

  const keysForTitleEvaluation = ['type', 'content'];
  const keysForEtmFormat = ['type', 'validation', 'default', 'content'];

  const handleTypeEvaluation = (jsonObject: any, type_keys: string[], type_result: string) => {
    if (jsonObject) {
      for (const key in jsonObject) {
        if (!type_keys.includes(key)) {
          return '';
        }
      }
      return type_result;
    }
    return '';
  }

  return {
    keysForTitleEvaluation,
    keysForEtmFormat,
    handleTypeEvaluation
  };
}