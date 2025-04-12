with silver as (
    select * from {{ ref('silver-criptosinfo') }}
),

comprar as (
    select
        cripto,
        price,
        tedencia_preco,
        rsi_14,
        macd,
        ma_7,
        spread,
        ordem_livro_sinal,
        dominancia_btc,
        data_extracao,
        'comprar' AS recomendacao
    from silver
    where tedencia_preco = 'alta'
    and rsi_14 < 70
    and macd > 0
    and spread < 0.01
),

vender as (
    select 
        cripto,
        price,
        tedencia_preco,
        rsi_14,
        macd,
        ma_7,
        spread,
        ordem_livro_sinal,
        dominancia_btc,
        data_extracao,
        'vender' AS recomendacao
    from silver
    where tedencia_preco = 'baixa'
    and rsi_14 > 70
    and macd < 0
),

esperar as (
    select
        cripto,
        price,
        tedencia_preco,
        rsi_14,
        macd,
        ma_7,
        spread,
        ordem_livro_sinal,
        dominancia_btc,
        data_extracao,
        'esperar' AS recomendacao
    from silver
    where tedencia_preco = 'estavel'
    or spread > 0.05
)

select * from comprar 
union all
select * from vender
union all
select * from esperar