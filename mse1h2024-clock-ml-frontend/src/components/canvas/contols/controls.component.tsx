import { FC } from "react";
import { Button } from "../../button/button.component";
import css from "./controls.module.css";
import { Link } from "../../link/link.component";

interface IControls {
	onClear?: () => any;
}

export const Controls: FC<IControls> = ({ onClear }) => {
	return (
		<div className={css.controls}>
			<label>
				<p>Брокер</p>
				<input type="checkbox" />
			</label>

			<Button onClick={onClear}>Стереть все</Button>
			<Link to="/result">Отправить</Link>
		</div>
	);
};
