import './auth-widget.scss';
import PropTypes from 'prop-types';
import React from 'react';
import assetman from '@pytsite/assetman';
import {lang} from '@pytsite/assetman';
import authApi from '@pytsite/auth-http-api';
import Widget from '@pytsite/widget2/components/widget';

export default class AuthWidget extends Widget {
    static propTypes = Object.assign({}, Widget.propTypes, {
        driverName: PropTypes.string.isRequired,
        href: PropTypes.string.isRequired,
    });

    constructor(props) {
        super(props);

        this.state = {
            error: null,
            isInitialized: false,
            isUserAuthenticated: false,
        }
    }

    _authenticate(code, state) {
        return authApi.signIn({driver: this.props.driverName, code: code, state: state})
    }

    componentDidMount() {
        const parsedLocation = assetman.parseLocation();
        const query = parsedLocation.query;

        authApi.me().then(() => {
            this.setState({
                isInitialized: true,
                isUserAuthenticated: true
            });
        }).catch(e => {
            if (query.code && query.state) {
                this._authenticate(query.code, query.state).then(r => {
                    delete query.code;
                    delete query.state;
                    const redirectUrl = parsedLocation.origin + parsedLocation.pathname;
                    window.location.href = assetman.url(redirectUrl, query);
                }).catch(e => {
                    if (e.hasOwnProperty('responseJSON') && e.responseJSON.hasOwnProperty('error'))
                        this.setState({error: e.responseJSON.error});
                });
            }

            this.setState({
                isInitialized: true,
            });
        });
    }

    render() {
        if (this.state.isUserAuthenticated)
            return (
                <div className={`${this.props.className} hidden`}></div>
            );

        const className = this.props.className + (this.state.isInitialized ? '' : ' hidden');
        return (
            <div className={className}>
                <div className="button">
                    <a href={this.props.href} title={lang.t('auth_id_gov_ua@sign_in_with_govid')}></a>
                </div>
                {this.state.error && (
                    <div className={'error-msg'}>{this.state.error}</div>
                )}
            </div>
        );
    }
}
