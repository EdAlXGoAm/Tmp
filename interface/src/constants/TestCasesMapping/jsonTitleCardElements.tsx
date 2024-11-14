import { useState } from 'react';

interface JsonTitleCardElementsProps {
  jsonPath: Array<string>;
  jsonKey: string;
  jsonValue: any;
  onSaveJson: (jsonPath: Array<string>, jsonKey: string, jsonValue: any) => void;
}

export const jsonTitleCardElements = ({ jsonPath, jsonKey, jsonValue, onSaveJson }: JsonTitleCardElementsProps) => {

  const [elementToEditType, setElementToEditType] = useState<{ key: string, value: string } | null>(null);
  const [isOpenExternalType, setIsOpenExternalType] = useState(false);

  const onCleanDataType = () => {
    setElementToEditType(null);
  }

  const onEditType = (key: string, value: string) => {
    setElementToEditType({ key, value });
    setIsOpenExternalType(true);
  }
  
  const onUpdateType = (key: string, value: string) => {
    let newJsonValue = { ...jsonValue, [key]: value };
    if (value === 'string') {
      newJsonValue = { ...newJsonValue, content: '' };
    }
    else {
      newJsonValue = { ...newJsonValue, content: [] };
    }
    onSaveJson(jsonPath, jsonKey, newJsonValue);
  }

  return {
    elementToEditType, setElementToEditType,
    isOpenExternalType, setIsOpenExternalType,
    onCleanDataType,
    onEditType,
    onUpdateType
  };
}