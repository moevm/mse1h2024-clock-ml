import { atomWithStorage, createJSONStorage } from "jotai/utils";

const storage = createJSONStorage<boolean>(() => localStorage);
export const brokerAtom = atomWithStorage<boolean>("broker", false, storage);
