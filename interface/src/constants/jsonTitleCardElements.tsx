export const jsonTitleCardElements = () => {

  const isNestedObject = (value: any) => {
    // Evaluate if any element in the object is a nested object
    for (const key in value) {
      console.log('typeof(', key, '):', typeof value[key]);
      if (!(typeof value[key] === 'string' ||
          typeof value[key] === 'number' ||
          typeof value[key] === 'boolean' ||
          typeof value[key] === null ||
          Array.isArray(value[key]))) {
        return true;
      }
    }
    return false;
  }

  return {
    isNestedObject
  };
}