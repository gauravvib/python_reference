# check how much nan is present in df
def intitial_eda_checks(df):
    '''
    Takes df
    Checks nulls
    '''
    if df.isnull().sum().sum() > 0:
        mask_total = df.isnull().sum().sort_values(ascending=False) 
        total = mask_total[mask_total > 0]

        mask_percent = df.isnull().mean().sort_values(ascending=False) 
        percent = mask_percent[mask_percent > 0] 

        missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    
        print(f'Total and Percentage of NaN:\n {missing_data}')
    else: 
        print('No NaN found.')
        
# list of cols with threshold of missing vals
def view_columns_w_many_nans(df, missing_percent):
    '''
    Checks which columns have over specified percentage of missing values
    Takes df, missing percentage
    Returns columns as a list
    '''
    mask_percent = df.isnull().mean()
    series = mask_percent[mask_percent > missing_percent]
    columns = series.index.to_list()
    print(columns) 
    return columns

# drop cols with threshold of missing vals
def drop_columns_w_many_nans(df, missing_percent):
    '''
    Takes df, missing percentage
    Drops the columns whose missing value is bigger than missing percentage
    Returns df
    '''
    series = view_columns_w_many_nans(df, missing_percent=missing_percent)
    list_of_cols = series.index.to_list()
    df.drop(columns=list_of_cols)
    print(list_of_cols)
    return df

# distr of all numerical cols
def histograms_numeric_columns(df, numerical_columns):
    '''
    Takes df, numerical columns as list
    Returns a group of histagrams
    '''
    import seaborn as sns
    f = pd.melt(df, value_vars=numerical_columns) 
    g = sns.FacetGrid(f, col='variable',  col_wrap=4, sharex=False, sharey=False)
    g = g.map(sns.distplot, 'value')
    return g

# heatmap for correlation between DV and numeric IDVs
def heatmap_numeric_w_dependent_variable(df, dependent_variable):
    '''
    Takes df, a dependant variable as str
    Returns a heatmap of all independent variables' correlations with dependent variable 
    '''
    plt.figure(figsize=(8, 10))
    g = sns.heatmap(df.corr()[[dependent_variable]].sort_values(by=dependent_variable), 
                    annot=True, 
                    cmap='coolwarm', 
                    vmin=-1,
                    vmax=1) 
    return g

# return numerical cols from df
def numerical_cols(df):
    df_num = df.select_dtypes(include = ['float64', 'int64'])
    num_cols = df_num.cols
    return num_cols

# plot histogram of all numerical cols from df (check datatype first)
def plt_hist_numerical(df):
    df_num = df.select_dtypes(include = ['float64', 'int64'])
    df_num.hist(figsize=(16, 20), bins=50, xlabelsize=8, ylabelsize=8);
    
# plot distribution of all categorical cols from df (check datatype first)
def plt_hist_cat(df):
    cols_not_num = [x for x in df.columns if x not in df.select_dtypes(include = ['float64', 'int64']).columns]
    df_not_num = df[cols_not_num]
    for i, ax in enumerate(fig.axes):
        if i < len(df_not_num.columns):
            ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=45)
            sns.countplot(x=df_not_num.columns[i], alpha=0.7, data=df_not_num, ax=ax)
    fig.tight_layout()    
    
# plot pair plots of dependent var with each of independent vars for checking whether outliers are affecting the correlation
# give required col names to be included for this analysis
def pair_plots_idv_dv(df, idv_cols, dv_col):
    import seaborn as sns
    for i in range(0, len(idv_cols), 5):
        sns.pairplot(data=df,
                    x_vars=df[idv_cols].columns[i:i+5],
                    y_vars=dv_col)

    

             
