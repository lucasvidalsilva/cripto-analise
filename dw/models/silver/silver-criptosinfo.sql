with source as (
    select
        *,
        lag(price) over (partition by cripto order by data_extracao) as price_anterior
    from
        {{ source('postgres', 'bronze-criptosinfo')     }}
),

metricas as (
    select
        cripto,
        price,
        high,
        low,
        bid,
        ask,
        volume,
        quote_volume,
        order_book_bid,
        order_book_ask,
        data_extracao,
        -- tedencia de preço
        case when price > price_anterior then 'alta' when price < price_anterior then 'baixa' else 'estavel' end as tedencia_preco,
        -- rsi 14
        avg(price) over (partition by cripto order by data_extracao rows between 13 preceding and current row) as rsi_14,
        -- macd
        avg(price) over (partition by cripto order by data_extracao rows between 11 preceding and current row) - avg(price) over (partition by cripto order by data_extracao rows between 25 preceding and current row) as macd,
        -- ma 7
        avg(price) over (partition by cripto order by data_extracao rows between 6 preceding and current row) as ma_7,
        -- spread
        (ask - bid) as spread,
        -- ordem livre
        case when order_book_bid > price then 'compra forte' when order_book_ask < price then 'venda forte' else 'neutro' end as ordem_livro_sinal,
        -- dominancia btc
        price / sum(price) over (partition by data_extracao) as dominancia_btc
    from 
        source
)

select * from metricas