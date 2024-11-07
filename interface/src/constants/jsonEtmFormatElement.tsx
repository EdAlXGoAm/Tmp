import { useState } from 'react';

export const jsonEtmFormatCardElements = () => {

  const [elementToEditType, setElementToEditType] = useState<{ key: string, value: string } | null>(null);
  const [isOpenExternalType, setIsOpenExternalType] = useState(false);

  const onCleanData = () => {
    setElementToEditType(null);
  }

  const handleEditType = (key: string, value: string) => {
    setElementToEditType({ key, value });
    setIsOpenExternalType(true);
  }

  return {
    elementToEditType, setElementToEditType,
    isOpenExternalType, setIsOpenExternalType,
    onCleanData,
    handleEditType
  };
}