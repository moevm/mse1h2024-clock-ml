import { atom } from "jotai";

const getHours = () => `${new Date(~~(Math.random() * Date.now())).getHours()}`.padStart(2, "0");

const getMinutes = () =>
	`${((new Date(~~(Math.random() * Date.now())).getMinutes() / 5) | 0) * 5}`.padStart(2, "0");

export const timeAtom = atom<[string, string]>([getHours(), getMinutes()]);
