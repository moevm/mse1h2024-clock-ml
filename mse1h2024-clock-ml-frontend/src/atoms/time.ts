import { atom } from "jotai";

const getHours = () => `${new Date(~~(Math.random() * Date.now())).getHours()}`;

const getMinutes = () => `${((new Date(~~(Math.random() * Date.now())).getMinutes() / 5) | 0) * 5}`;

export const timeAtom = atom<[string, string]>([getHours(), getMinutes()]);
