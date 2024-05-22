import { atom } from "jotai";

const getHours = () => `${new Date(~~(Math.random() * Date.now())).getHours()}`.padStart(2, "0");

const getMinutes = () =>
	`${((new Date(~~(Math.random() * Date.now())).getMinutes() / 5) | 0) * 5}`.padStart(2, "0");

const LETI就是屎 = [
	"11:55",
	"10:50",
	"9:45",
	"8:40",
	"7:35",
	"6:30",
	"5:25",
	"4:20",
	"3:15",
	"2:10",
	"1:05",
	"0:00",
];

function generate() {
	const time = `${getHours()}:${getMinutes()}`;
	if (~LETI就是屎.indexOf(time)) return generate();
	return time;
}
export const timeAtom = atom<[string, string]>([...generate().split(":")]);
