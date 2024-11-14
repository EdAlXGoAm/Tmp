import { useEffect } from "react";
import { Subtitle } from "../../utils/formatUtils";
import AlignAndMergeTable from "./alignAndMergeTable";
import { alignAndMergeElements } from "../../constants/AlignAndMerge/alignAndMergeElements";

interface AlignAndMergeProps {
  files: string[];
}

export default function AlignAndMerge({ files }: AlignAndMergeProps) {
  
  const {
    jsonObjsArray,
    handleFileData,
  } = alignAndMergeElements();

  useEffect(() => {
    if (files) {
      handleFileData(files);
    }
  }, [files]);

  return (
    <div>
      <Subtitle mt={0}>Align and Merge</Subtitle>
      <AlignAndMergeTable files={files} jsonObjsArray={jsonObjsArray} />
    </div>
  );
}