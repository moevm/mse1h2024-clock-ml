import { FC, MouseEvent } from "react";
import { Button } from "../../button/button.component";
import css from "./controls.module.css";
import { Link } from "../../link/link.component";
import { useAtom } from "jotai";
import { brokerAtom } from "../../../atoms/broker";

interface IControls {
	onClear?: () => void;
	onSubmit?: (e: MouseEvent) => void;
}

export const Controls: FC<IControls> = ({ onClear, onSubmit }) => {
	const [broker, setBroker] = useAtom(brokerAtom);

	return (
		<div className={css.controls}>
			<label>
				<p>Брокер</p>
				<input type="checkbox" checked={broker} onChange={() => setBroker((a) => !a)} />
			</label>

			<Button onClick={onClear}>Стереть все</Button>
			<Link to="/result" onClick={onSubmit}>
				Отправить
			</Link>
		</div>
	);
};
