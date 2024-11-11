import React, { useEffect} from 'react';
import styles from '../../styles/TypeForm.module.css';
import { TypeFormElements } from '../../constants/forms/typeFormElements';
import { RowForm } from '../../utils/formatUtils';

interface TypeFormProps {
  elementToEdit?: any;
  onCleanData: () => void;
  isOpenExternal: boolean;
  setIsOpenExternal: React.Dispatch<React.SetStateAction<boolean>>;
  updateType: (key: string, value: string) => void;
  createType: (value: string) => void;
}

const TypeForm: React.FC<TypeFormProps> = ({
  elementToEdit,
  onCleanData,
  isOpenExternal,
  updateType,
  createType
}) => {
  const {
    isOpen, setIsOpen,
    error,
    loading,
    formData, setFormData,
    handleChange,
    handleSubmit,
    handleClose
  } = TypeFormElements({ onCleanData, elementToEdit, updateType, createType });

  useEffect(() => {
    if(elementToEdit) {
      setFormData(elementToEdit.value);
      setIsOpen(true);
    }
  }, [elementToEdit]);

  useEffect(() => {
    setIsOpen(isOpenExternal);
  }, [isOpenExternal]);

  return (
    <>
      {isOpen && (
        <div className={styles.overlay} onClick={handleClose}>
          <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
            <h2>{elementToEdit ? 'Edit Type' : 'Add Type'}</h2>
            <form onSubmit={handleSubmit}>
              <RowForm>
                <label>Type</label>
                <select
                  name="type"
                  value={formData}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select a type</option>
                  <option value="string">string</option>
                  <option value="array">array</option>
                </select>
              </RowForm>
              {error && <p className={styles.error}>{error}</p>}
              <div className={styles.buttons}>
                <button type="submit" disabled={loading}>
                  {loading ? 'Updating...' : (elementToEdit ? 'Update' : 'Add')}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
};

export default TypeForm;
