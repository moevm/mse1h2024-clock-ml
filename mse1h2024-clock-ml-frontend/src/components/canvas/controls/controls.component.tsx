import { FC, MouseEvent } from "react";
import { Button } from "../../button/button.component";
import css from "./controls.module.css";
import { Link } from "../../link/link.component";
import { useAtom, useAtomValue } from "jotai";
import { brokerAtom } from "../../../atoms/broker";
import { timeAtom } from "../../../atoms/time";

interface IControls {
	onClear?: () => void;
	onSubmit?: (e: MouseEvent) => void;
}

export const Controls: FC<IControls> = ({ onClear, onSubmit }) => {
	const [broker, setBroker] = useAtom(brokerAtom);
	const time = useAtomValue(timeAtom);

	return (
		<div className={css.controls}>
			<p>Нарисуйте {time.join(":")}</p>
			<label>
				<p>Брокер</p>
				<input type="checkbox" checked={broker} onChange={() => setBroker((a) => !a)} />
			</label>

			<Button onClick={onClear} id="canvas-clear">
				Стереть все
			</Button>
			<Link to="/result" onClick={onSubmit}>
				Отправить
			</Link>
		</div>
	);
};
