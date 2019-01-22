#!/bin/sh

http get kong-admin:8001 && \
http --ignore-stdin put kong-admin:8001/services/user host=user port=8089 protocol=http -f && \
http --ignore-stdin put kong-admin:8001/services/shop host=shop port=8090 protocol=http -f && \
http --ignore-stdin put kong-admin:8001/services/promotion host=promotion port=8091 protocol=http -f && \
http --ignore-stdin post kong-admin:8001/services/user/routes name=user methods:='["GET"]' protocols:='["http"]' && \
http --ignore-stdin post kong-admin:8001/services/shop/routes name=shop methods:='["GET"]' protocols:='["http"]' && \
http --ignore-stdin post kong-admin:8001/services/promotion/routes name=promotion methods:='["GET"]' protocols:='["http"]'