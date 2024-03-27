import { useEffect, useState } from "react";
import { Loader } from "../../components/loader/loader.component";
import { Result } from "../../components/result/result.component";
import { Layout } from "../../components/layout/layout.component";
import { useAtomValue } from "jotai";
import { scoreAtom } from "../../atoms/score";

export const ResultPage = () => {
	const [loading, setLoading] = useState(true);
	const score = useAtomValue(scoreAtom);

	useEffect(() => {
		if (typeof score === "number") {
			setLoading(false);
		}
	}, [score]);

	return <Layout>{loading ? <Loader /> : <Result score={score} />}</Layout>;
};
