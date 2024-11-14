import { useState } from "react";
import { open } from '@tauri-apps/plugin-dialog';
import { CenteredColumn, CustomForm, Subtitle, Titles } from "./utils/formatUtils";
import AlignAndMerge from "./components/AlignAndMerge/alignAndMerge";
import { Button } from "@mui/material";

export default function TestCasesAlignAndMerge() {
  const [files, setFiles] = useState<String[]>([]);

  const handleFileChange = async () => {
    const selectedFile = await open({
      filters: [{ name: 'JSON Files', extensions: ['json'] }],
      defaultPath: 'D:/edalxgoam/Tmp/MAPP'
    });
    if (selectedFile) {
      setFiles(prevFiles => [...prevFiles, selectedFile as string]);
    }
  };

  const splitAndFormatString = (file: string) => {
    const fileString = file.split('\\');
    if (fileString.length > 3) {
      return `${fileString[0]}\\${fileString[1]}\\...\\${fileString[fileString.length - 1]}`;
    }
    return file;
  };

  return (
    <div className="container-fluid">
      <Titles>
      <h1>Test Cases Align and Merge</h1>
      </Titles>
      <Subtitle>Drag and Drop or Select the JSON file</Subtitle>
      <CenteredColumn mt={0}>
      <div className="FileContainer">
        <button onClick={handleFileChange}>Select JSON File</button>

        <label className="labelFormCustom">Selected file: </label>
        {files && files.map((file, i) => (
          <CustomForm key={i}>
            <input className="inputFormCustom" type="text" readOnly style={{width: 'calc(100% - 100px)'}}
              value={splitAndFormatString(file as string)}
            />
            <Button variant="contained" color="error"
              onClick={() => setFiles(prevFiles => prevFiles.filter(prevFile => prevFile !== file))}
              style={{
                padding: '0px 10px',
                marginLeft: '10px'
              }}
            >Remove</Button>
          </CustomForm>
        ))}
        <Button color="error"
          onClick={() => setFiles([])}
          style={{
            padding: '0px 10px',
            marginTop: '10px'
          }}
        >Clear</Button>
        </div>
      </CenteredColumn>
      <CenteredColumn mt={3} width={12}>
        <AlignAndMerge key={files.join(',')} files={files as string[]} />
      </CenteredColumn>
    </div>
  );
}
