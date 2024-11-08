import { useState } from 'react';

interface JsonEtmFormatCardElementsProps {
  jsonPath: Array<string>;
  jsonKey: string;
  jsonValue: any;
  onSaveJson: (jsonPath: Array<string>, jsonKey: string, jsonValue: any) => void;
}

export const jsonEtmFormatCardElements = ({ jsonPath, jsonKey, jsonValue, onSaveJson }: JsonEtmFormatCardElementsProps) => {

  const [elementToEditType, setElementToEditType] = useState<{ key: string, value: string } | null>(null);
  const [isOpenExternalType, setIsOpenExternalType] = useState(false);

  const onCleanDataType = () => {
    setElementToEditType(null);
  }

  const handleEditType = (key: string, value: string) => {
    setElementToEditType({ key, value });
    setIsOpenExternalType(true);
  }
  
  const onUpdateType = (key: string, value: string) => {
    let newJsonValue = { ...jsonValue, [key]: value };
    if (value === 'string') {
      if (Array.isArray(newJsonValue.default) && newJsonValue.default.length === 0) {
        newJsonValue = { ...newJsonValue, default: '' };
      }
      else if (Array.isArray(newJsonValue.default)) {
        const newStringForDefault = newJsonValue.default.join(', ');
        newJsonValue = { ...newJsonValue, default: newStringForDefault };
      }
    }
    else if (value === 'array') {
      if (newJsonValue.default === '') {
        newJsonValue = { ...newJsonValue, default: [] };
      }
      else if (typeof newJsonValue.default === 'string') {
        const newArrayForDefault = newJsonValue.default.split(', ');
        newJsonValue = { ...newJsonValue, default: newArrayForDefault };
      }
    }
    onSaveJson(jsonPath, jsonKey, newJsonValue);
  }

  const [elementToEditValidation, setElementToEditValidation] = useState<{ key: string, value: any } | null>(null);
  const [isOpenExternalValidation, setIsOpenExternalValidation] = useState(false);

  const onCleanDataValidation = () => {
    setElementToEditValidation(null);
  }

  const handleEditValidation = (key: string, value: any) => {
    setElementToEditValidation({ key, value });
    setIsOpenExternalValidation(true);
  }

  const onUpdateValidation = (key: string, value: any) => {
    let newJsonValue = { ...jsonValue, [key]: value };
    onSaveJson(jsonPath, jsonKey, newJsonValue);
  }

  const [elementToEditDefault, setElementToEditDefault] = useState<{ key: string, value: any, type: boolean, validation: string[] | string } | null>(null);
  const [isOpenExternalDefault, setIsOpenExternalDefault] = useState(false);

  const onCleanDataDefault = () => {
    setElementToEditDefault(null);
  }

  const handleEditDefault = (key: string, value: any, type: boolean, validation: string[] | string) => {
    setElementToEditDefault({ key, value, type, validation });
    setIsOpenExternalDefault(true);
  }

  const onUpdateDefault = (key: string, value: any) => {
    let newJsonValue = { ...jsonValue, [key]: value };
    onSaveJson(jsonPath, jsonKey, newJsonValue);
  }

  const [elementToEditContent, setElementToEditContent] = useState<{ key: string, value: any } | null>(null);
  const [isOpenExternalContent, setIsOpenExternalContent] = useState(false);

  const onCleanDataContent = () => {
    setElementToEditContent(null);
  }

  const handleEditContent = (key: string, value: any) => {
    setElementToEditContent({ key, value });
    console.log('value', value);
    setIsOpenExternalContent(true);
  }

  const onUpdateContent = (key: string, value: any) => {
    let newJsonValue = { ...jsonValue, [key]: value };
    onSaveJson(jsonPath, jsonKey, newJsonValue);
  }

  return {
    elementToEditType, setElementToEditType,
    isOpenExternalType, setIsOpenExternalType,
    onCleanDataType,
    handleEditType,
    onUpdateType,
    elementToEditValidation, setElementToEditValidation,
    isOpenExternalValidation, setIsOpenExternalValidation,
    onCleanDataValidation,
    handleEditValidation,
    onUpdateValidation,
    elementToEditDefault, setElementToEditDefault,
    isOpenExternalDefault, setIsOpenExternalDefault,
    onCleanDataDefault,
    handleEditDefault,
    onUpdateDefault,
    elementToEditContent, setElementToEditContent,
    isOpenExternalContent, setIsOpenExternalContent,
    onCleanDataContent,
    handleEditContent,
    onUpdateContent
  };
}