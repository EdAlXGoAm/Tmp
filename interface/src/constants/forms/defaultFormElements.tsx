import React, { useState } from 'react';

interface DefaultFormElementsProps {
  onCleanData: () => void;
  elementToEdit: { key: string, value: any, type: boolean, validation: string[] | string } | null;
  updateDefault: (key: string, value: any) => void;
  createDefault: (value: string) => void;
}

export const DefaultFormElements = ({ onCleanData, elementToEdit, updateDefault, createDefault }: DefaultFormElementsProps) => {
  
  const emptyElementData = {
    type: false, // false: string, true: array
    value: [] as string[] // array of strings
  }

  const [isOpen, setIsOpen] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const [formData, setFormData] = useState(emptyElementData);
  
  const handleClose = () => {
    setError(null);
    setIsOpen(false);
    setFormData(emptyElementData);
    onCleanData();
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { value } = e.target;
    if (formData.type) {
      if (e.target.name === 'value') {
        setFormData((prevData: any) => ({ ...prevData, value: value.split(', ') }));
      } else { // value[index]
        setFormData((prevData: any) => ({ ...prevData, 
          value: prevData.value.map((validation: string, index: number) => 
            index === parseInt(e.target.name.split('[')[1].split(']')[0]) ? value : validation
          )
        }));
      }
    } else {
      setFormData((prevData: any) => ({ ...prevData, value }));
    }
  }

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    try {
      if(elementToEdit) {
        updateDefault(elementToEdit.key, formData.value);
      } else {
        createDefault(formData.value.join(', '));
      }
      handleClose();
    } catch (error) {
      setError("Error al crear el default");
    } finally {
      setLoading(false);
    }
  }

  return {
    emptyElementData,
    isOpen, setIsOpen,
    error, setError,
    loading, setLoading,
    formData, setFormData,
    handleChange,
    handleSubmit,
    handleClose
  }
}
