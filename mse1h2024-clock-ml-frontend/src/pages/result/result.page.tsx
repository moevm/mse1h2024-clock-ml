import { useEffect, useState } from "react";
import { Loader } from "../../components/loader/loader.component";
import { Result } from "../../components/result/result.component";
import { Layout } from "../../components/layout/layout.component";

export const ResultPage = () => {
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		new Promise((r) => setTimeout(r, 5000)).then(() => {
			setLoading(false);
		});
	}, []);

	return (
		<Layout>
			{loading && <Loader />}
			{!loading && <Result />}
		</Layout>
	);
};
