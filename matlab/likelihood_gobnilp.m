function [LL] = likelihood_gobnilp(graphFile, dataFile)

 dag = dlmread(graphFile);
 data = transpose(dlmread(dataFile)) + 1;

 bnet = mk_bnet(dag, 2*ones(1,9));

 for i = 1:9
			bnet.CPD{i} = tabular_CPD(bnet, i, 'prior_type', 'dirichlet', 'dirichlet_weight', 1);
 end

 LL = log_marg_lik_complete(bnet, data);
