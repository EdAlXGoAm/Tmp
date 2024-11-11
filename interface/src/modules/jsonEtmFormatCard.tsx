import { Row, Column, VariableText, VariableTextBorder, VariableArray, VariableArrayMinimalist } from '../utils/formatUtils';
import { jsonEtmFormatCardElements } from '../constants/jsonEtmFormatElement';
import TypeForm from './forms/typeForm';
import ValidationForm from './forms/validationForm';
import DefaultForm from './forms/defaultForm';
import ContentForm from './forms/contentForm';
interface JsonEtmFormatCardProps {
  jsonPath: Array<string>;
  jsonKey: string;
  jsonValue: any;
  onSaveJson: (jsonPath: Array<string>, jsonKey: string, jsonValue: any) => void;
}

export const JsonEtmFormatCard: React.FC<JsonEtmFormatCardProps> = ({ jsonPath, jsonKey, jsonValue, onSaveJson }) => {
  const {
    elementToEditType,
    isOpenExternalType, setIsOpenExternalType,
    onCleanDataType,
    handleEditType,
    onUpdateType,
    elementToEditValidation,
    isOpenExternalValidation, setIsOpenExternalValidation,
    onCleanDataValidation,
    handleEditValidation,
    onUpdateValidation,
    elementToEditDefault,
    isOpenExternalDefault, setIsOpenExternalDefault,
    onCleanDataDefault,
    handleEditDefault,
    onUpdateDefault,
    elementToEditContent,
    isOpenExternalContent, setIsOpenExternalContent,
    onCleanDataContent,
    handleEditContent,
    onUpdateContent
  } = jsonEtmFormatCardElements({ jsonPath, jsonKey, jsonValue, onSaveJson });

  return (
    <>
      <TypeForm
        onCleanData={onCleanDataType}
        elementToEdit={elementToEditType}
        isOpenExternal={isOpenExternalType}
        setIsOpenExternal={setIsOpenExternalType}
        updateType={onUpdateType}
        createType={() => null}
      />
      <ValidationForm
        onCleanData={onCleanDataValidation}
        elementToEdit={elementToEditValidation}
        isOpenExternal={isOpenExternalValidation}
        setIsOpenExternal={setIsOpenExternalValidation}
        updateValidation={onUpdateValidation}
        createValidation={() => null}
      />
      <DefaultForm
        onCleanData={onCleanDataDefault}
        elementToEdit={elementToEditDefault}
        isOpenExternal={isOpenExternalDefault}
        setIsOpenExternal={setIsOpenExternalDefault}
        updateDefault={onUpdateDefault}
        createDefault={() => null}
      />
      <Row mt={1} mb={2}>
        <Column>
          {/* <CodeContainer code={`${JSON.stringify(jsonValue, null, 2)}`} /> */}
          {jsonValue && typeof jsonValue === 'object' && (
            <>
              {Object.entries(jsonValue).map(([key, value], i) => (
                <div key={i}>
                  {/* TYPE (string) */}
                  {key === 'type' && typeof value === 'string' ? (
                    <VariableText variable={'type'} value={value} onClick={() => handleEditType(key, value)}/>
                  ) : /* VALIDATION (string) */
                    key === 'validation' && typeof value === 'string' ? (
                    <VariableText variable={key} value={value} onClick={() => handleEditValidation(key, value)}/> // TODO: Add onClick
                  ) : /* VALIDATION (object-array) */
                  key === 'validation' && typeof value === 'object' && Array.isArray(value) ? (
                    <VariableArrayMinimalist variable={key} value={value} onClick={() => handleEditValidation(key, value)}/> // TODO: Add onClick
                  ) : /* DEFAULT (string) */
                  key === 'default' && typeof value === 'string' ? (
                    <VariableTextBorder variable={key} value={value} color={'#f11f00'} onClick={() => handleEditDefault(key, value, false, jsonValue.validation)}/> // TODO: Add onClick
                  ) : /* DEFAULT (object-array) */
                  key === 'default' && typeof value === 'object' && Array.isArray(value) ? (
                    <VariableArray variable={key} value={value} color={'#f11f00'} onClick={() => handleEditDefault(key, value, true, jsonValue.validation)}/> // TODO: Add onClick
                  ) : /* CONTENT (object-array) */
                  key === 'content' && typeof value === 'object' && Array.isArray(value) ? (
                    <>
                      <VariableArray variable={key} value={value} color={'#f11f00'} onClick={() => handleEditContent(key, value)}/>
                      {isOpenExternalContent && (
                        <ContentForm
                          onCleanData={onCleanDataContent}
                          elementToEdit={elementToEditContent}
                          isOpenExternal={isOpenExternalContent}
                          setIsOpenExternal={setIsOpenExternalContent}
                          updateContent={onUpdateContent}
                          createContent={() => null}
                        />
                      )}
                    </>
                  ) : null}
                </div>
              ))}
            </>
          )}
        </Column>
      </Row>
    </>
  );
}