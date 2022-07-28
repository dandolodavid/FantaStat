import pandas as pd
import numpy as np
import math
from scipy.stats import poisson
from scipy.optimize import minimize

def poisson_density(x,lam):
    return np.exp(-lam) * lam**x/ math.factorial(x) 
    
def rho_correction(x, y, lambda_x, mu_y, rho):
    if x==0 and y==0:
        return 1- (lambda_x * mu_y * rho)
    elif x==0 and y==1:
        return 1 + (lambda_x * rho)
    elif x==1 and y==0:
        return 1 + (mu_y * rho)
    elif x==1 and y==1:
        return 1 - rho
    else:
        return 1

def dixon_coles_loglike(x, y, alpha_h, beta_h, alpha_a, beta_a, rho, gamma, t, xi=0):
    lambda_x = np.exp(alpha_h + beta_a + gamma)
    lambda_y = np.exp(alpha_a + beta_h) 
    return ( np.exp(-xi*t) * np.log(rho_correction(x, y, lambda_x, lambda_y, rho) ) +  np.log(poisson_density(x, lambda_x) ) + np.log(poisson_density(y, lambda_y) ) )

def compute_log_likelihood(params, n_teams, dataset, teams, xi, ):
    
        atk_coefs = pd.DataFrame( data = { 'Atk_Params' : params[:n_teams] }, index= teams )
        def_coefs = pd.DataFrame( data = { 'Def_Params' :  params[n_teams : (2*n_teams) ] }, index= teams ) 
        rho, gamma = params[-2:]
        
        log_likelihood = dataset.apply(lambda row: dixon_coles_loglike(row.HomeGol, row.AwayGol,
                                                                atk_coefs.loc[row.HomeTeam].values[0], def_coefs.loc[row.HomeTeam].values[0],
                                                                atk_coefs.loc[row.AwayTeam].values[0], def_coefs.loc[row.AwayTeam].values[0], 
                                                               rho, gamma, row.TimeDiff, xi ), axis=1 )
        return -sum(log_likelihood)

def solve_parameters(dataset, home_team = 'HomeTeam', away_team='AwayTeam', home_gol = 'HomeGol', away_gol = 'AwayGol', date='Date', init=None, options={'disp': True, 'maxiter':100}, xi = 0 ):
    
    model_data = dataset.rename(columns= {home_team:'HomeTeam',away_team:'AwayTeam',home_gol:'HomeGol',away_gol:'AwayGol', date:'Date'} ).copy()
    model_data.Date = pd.to_datetime( model_data.Date )
    model_data['TimeDiff'] =  model_data.Date.apply(lambda x: (model_data.Date.max() - x).days )
    
    home_teams = np.sort(dataset['HomeTeam'].unique())
    away_teams = np.sort(dataset['AwayTeam'].unique())
    n_teams = len(home_teams)
    
    if init is None:
        # random initialisation of model parameters
        init = np.concatenate((np.random.uniform(0.1,1,(n_teams)), # attack strength
                                np.random.uniform(-0.1,-1,(n_teams)), # defence strength
                                np.array([ 0.1, 1 ]) # rho (score correction), gamma (home advantage)
                                ))

    constraints = [ {'type':'eq', 'fun': lambda x: sum(x[:n_teams-1]) - x[n_teams] } ]
    optim = minimize(compute_log_likelihood, x0 = init, constraints = constraints, args= (n_teams, model_data, home_teams, xi ), options=options )
    
    out = pd.DataFrame( data = { 'Atk_Params':optim.x[0:n_teams] +1, 'Def_Params':optim.x[n_teams:2*n_teams] -1 }, index = home_teams )
    rho, home = optim.x[-2:]
    
    return out, rho, home

