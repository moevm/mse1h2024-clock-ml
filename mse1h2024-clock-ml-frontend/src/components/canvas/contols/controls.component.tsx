import { FC, MouseEvent } from "react";
import { Button } from "../../button/button.component";
import css from "./controls.module.css";
import { Link } from "../../link/link.component";

interface IControls {
	onClear?: () => any;
	onSubmit?: (e: MouseEvent) => any;
}

export const Controls: FC<IControls> = ({ onClear, onSubmit }) => {
	return (
		<div className={css.controls}>
			<label>
				<p>Брокер</p>
				<input type="checkbox" />
			</label>

			<Button onClick={onClear}>Стереть все</Button>
			<Link to="/result" onClick={onSubmit}>
				Отправить
			</Link>
		</div>
	);
};
