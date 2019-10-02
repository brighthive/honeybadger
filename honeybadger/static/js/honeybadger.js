$(function () {
    $.ajaxSetup({
        contentType: "application/json"
    });

    setNavLink();

    try {
        appLoading = true;
        preloadMCIFormFields().then(function () {
            $('#ethnicity-race').attr('size', $('#ethnicity-race option').length);
            appLoading = false;
        }).catch(function () {
            ;
        });
    } catch (e) {
        showNotice('Error', 'There was an error loading the page.');
    }

    try {
        appLoading = true;
        preloadReferralFormFields().then(function () {
            appLoading = false;
        }).catch(function () {
            ;
        });
    } catch (e) {
        showNotice('Error', 'There was an error loading the page.');
    }

    function showNotice(title, body) {
        alert(body);
    }

    function setNavLink() {
        let path = location.pathname;
        path = decodeURIComponent(path.replace(/\/$/, '')).split('/');
        if (path.length == 1) {
            path = '/';
        } else {
            path = `/${path[1]}`;
        }
        $('.nav-link').removeClass('active');
        $('.nav-link').each(function () {
            let href = $(this).attr('href');
            if (href !== undefined) {
                if (path.length === 0) {
                    $(this).addClass('active');
                    return false;
                } else if (href.substring(0, path.length) === path) {
                    $(this).addClass('active');
                    return false;
                }
            }
        });
    }

    async function preloadMCIFormFields() {
        await Promise.all([
            appendOption('/mci/gender', '#gender', 'gender', 'gender'),
            appendOption('/mci/ethnicity', '#ethnicity-race', 'ethnicity_Race', 'ethnicity_Race'),
            appendOption('/mci/education_level', '#education-level', 'education_level', 'education_level'),
            appendOption('/mci/employment_status', '#employment-status', 'employment_status', 'employment_status'),
            appendOption('/mci/provider', '#provider', 'provider_name', 'provider_name'),
            appendOption('/mci/country', '#country', 'country', 'country'),
            appendOption('/mci/state', '#state', 'state', 'state')
        ]);
    }

    async function preloadReferralFormFields() {
        await Promise.all([
            appendOption('/mci/provider', '#source-provider', 'provider_name', 'id'),
            appendOption('/mci/provider', '#destination-provider', 'provider_name', 'id'),
            appendOption('/mci/program', '#program', 'program_name', 'id')
        ]);
    }

    function initMCIForm() {
        return new Promise(function (resolve, reject) {
            resolve(function () {
                $('#mci-form').trigger('reset');
            });
            reject(function () {
                showNotice('Error', 'Failed to reset form.');
            });
        });
    }

    function initReferralForm() {
        return new Promise(function (resolve, reject) {
            resolve(function () {
                $('#referral-form').trigger('reset');
            });
            reject(function () {
                showNotice('Error', 'Failed to reset form.');
            });
        });
    }

    async function appendOption(url, id, val, label) {
        return $.getJSON(url, function (data) {
            $.each(data, function (_, value) {
                $(id).append(new Option(value[val], value[label]));
            });
        });
    }

    function startSpinner() {
        const spinner = $('#spinner');
        spinner.modal({ backdrop: 'static', keyboard: false }, 'toggle');
    }

    function stopSpinner() {
        const spinner = $('#spinner');
        spinner.modal('toggle');
    }

    function getDate() {
        const now = new Date();
        var day = ("0" + now.getDate()).slice(-2);
        var month = ("0" + (now.getMonth() + 1)).slice(-2);
        var today = now.getFullYear() + "-" + (month) + "-" + (day);
        return today;
    }

    /* User Management */
    function setUserFormDefaults() {
        $('#registration-date').val(getDate());
        $('#ethnicity-race').val(['Unknown']);
        $('#country').val('US');
        $('#education-level').val('Unknown');
        $('#employment-status').val('Unknown');
        $('#gender').val('Unknown');
        $('#provider').val('HoneyBadger');
    }

    $('.user-detail').click(function (event) {
        event.preventDefault();
        $('#create-buttons').hide();
        $('#edit-buttons').show();
        startSpinner();
        let url = $(this).attr('href');
        $.getJSON(url).then(function (data, err) {
            initMCIForm().then(function (_) {
                stopSpinner();
                $('#mci-form-modal').modal('toggle');
                $('#mci-id').val(data['mci_id']);
                $('#registration-date').val(data['registration_date']);
                $('#vendor-id').val(data['vendor_id']);
                $('#first-name').val(data['first_name']);
                $('#middle-name').val(data['middle_name']);
                $('#last-name').val(data['last_name']);
                $('#suffix').val(data['suffix']);
                $('#date-of-birth').val(data['date_of_birth']);
                $('#address').val(data['mailing_address']['address']);
                $('#city').val(data['mailing_address']['city']);
                $('#postal-code').val(data['mailing_address']['postal_code']);
                $('#email-address').val(data['email_address']);
                $('#telephone').val(data['telephone']);
                $('#gender').val(data['gender']);
                $('#state').val(data['mailing_address']['state']);
                $('#country').val(data['mailing_address']['country']);
                $('#education-level').val(data['education_level'].length > 0 ? data['education_level'] : 'Unknown');
                $('#ethnicity-race').val(data['ethnicity_race'].length > 0 ? data['ethnicity_race'] : ['Unknown']);
                $('#employment-status').val(data['employment_status'].length > 0 ? data['employment_status'] : ['Unknown']);
                $('#provider').val(data['source'].length > 0 ? data['source'] : '');
            }).catch(function (_) {
                showNotice('Error', 'Failed to load page.');
            });
        });
    });

    $('#add-user').click(function (event) {
        event.preventDefault();
        $('#create-buttons').show();
        $('#edit-buttons').hide();
        $('#mci-form').trigger('reset');
        initMCIForm().then(function (data, err) {
            if (appLoading) {
                startSpinner();
                setTimeout(function () {
                    stopSpinner();
                    $('#mci-form-modal').modal('toggle');
                    setUserFormDefaults();
                }, 3000);
            } else {
                $('#mci-form-modal').modal('toggle');
                setUserFormDefaults();
            }
        });
    });

    $('#clear-user-form').click(function (event) {
        event.preventDefault();
        $('#mci-form').trigger('reset');
        setUserFormDefaults();
    });

    $('#save-user').click(function (event) {
        event.preventDefault();
        const userForm = $('#mci-form')
        user = {
            'registration_date': $('#registration-date').val(),
            'vendor_id': $('#vendor-id').val(),
            'first_name': $('#first-name').val(),
            'middle_name': $('#middle-name').val(),
            'last_name': $('#last-name').val(),
            'suffix': $('#suffix').val(),
            'date_of_birth': $('#date-of-birth').val(),
            'gender': $('#gender').val(),
            'ethnicity_race': $('#ethnicity-race').val(),
            'mailing_address': {
                'address': $('#address').val(),
                'city': $('#city').val(),
                'country': $('#country').val(),
                'postal_code': $('#postal-code').val(),
                'state': $('#state').val()
            },
            'email_address': $('#email-address').val(),
            'telephone': $('#telephone').val(),
            'education_level': $('#education-level').val(),
            'employment_status': $('#employment-status').val(),
            'source': $('#provider').val(),
        };
        $.post('/mci/users', JSON.stringify(user)).done(function (response) {
            response = JSON.parse(response);
            if (response['match_probability'] !== undefined) {
                showNotice('MCI Match', `Found an existing user with match probability of ${response['match_probability']}. Assigned MCI ID to current record.`);
                $('#mci-id').val(response['mci_id']);
            } else {
                showNotice('User Created', 'Successfully created new MCI user.');
                $('#mci-id').val(response['mci_id']);
            }
        }).fail(function (data) {
            showNotice('Error', 'Failed to create new MCI user.');
        });
    });


    /**
     * Referral Management
     */

    function setReferralFormDefaults() {
        $('#referral-date').val(getDate());
    }

    $('.referral-detail').click(function (event) {
        event.preventDefault();
        $('#create-referral-buttons').hide();
        $('#edit-referral-buttons').show();
        startSpinner();
        let url = $(this).attr('href');
        $.getJSON(url).then(function (data, err) {
            initReferralForm().then(function (_) {
                stopSpinner();
                $('#referral-form-modal').modal('toggle');
                $('#referral-id').val(data['id']);
                $('#user-id').val(data['mci_id']);
                $('#referral-date').val(data['referral_date']);
                $('#program').val(data['program_id']);
                $('#source-provider').val(data['source_provider_id']);
                $('#destination-provider').val(data['destination_provider_id']);
                $('#recommended-date').val(data['recommended_date']);
                $('#accepted-date').val(data['accepted_date']);
                $('#completed-date').val(data['completed_date']);
                $('#serviced-date').val(data['serviced_date']);
                $('#referral-start-date').val(data['referral_start_date']);
                $('#referral-end-date').val(data['referral_end_date']);
            }).catch(function (_) {
                showNotice('Error', 'Failed to load page.');
            });
        });
    });

    $('#clear-referral-form').click(function (event) {
        event.preventDefault();
        const mciID = $('#user-id').val();
        $('#referral-form').trigger('reset');
        setReferralFormDefaults();
        $('#user-id').val(mciID);
    });

    $('#save-referral').click(function (event) {
        event.preventDefault();
        const referralForm = $('#referral-form');
        let referral = {
            'mci_id': $('#user-id').val(),
            'referral_date': $('#referral-date').val(),
            'program_id': parseInt($('#program').val()),
            'source_provider_id': parseInt($('#source-provider').val()),
            'destination_provider_id': parseInt($('#destination-provider').val()),
            'recommended_date': $('#recommended-date').val(),
            'accepted_date': $('#accepted-date').val(),
            'completed_date': $('#completed-date').val(),
            'serviced_date': $('#serviced-date').val(),
            'referral_start_date': $('#referral-start-date').val(),
            'referral_end_date': $('#referral-end-date').val()
        }
        $.each(referral, function (key, value) {
            if (value === '' || value === null) {
                delete referral[key];
            }
            return referral;
        });
        $.post('/referrals/', JSON.stringify(referral)).done(function () {
            showNotice('Referral Saved', 'Successfull saved referral.');
            $('#referral-form-modal').modal('toggle');
            location.reload();
        }).fail(function (data) {
            showNotice('Error', 'Failed to save referral.');
        });
    });

    $('#service-referral').click(function (event) {
        event.preventDefault();
        $('#serviced-date').val(getDate());
        const serviced_referral = {
            'serviced_date': $('#serviced-date').val()
        }
        $.post('/referrals/' + $('#referral-id').val(), JSON.stringify(serviced_referral)).done(function () {
            location.reload();
            showNotice('Successfult Serviced Referral', 'Successfully marked referral as serviced.');
        }).fail(function (data) {
            showNotice('Error', 'Failed to mark referral as serviced.');
        })
    });

    $('#update-referral').click(function (event) {
        event.preventDefault();
        const referralForm = $('#referral-form');
        let referral = {
            'mci_id': $('#user-id').val(),
            'referral_date': $('#referral-date').val(),
            'program_id': parseInt($('#program').val()),
            'source_provider_id': parseInt($('#source-provider').val()),
            'destination_provider_id': parseInt($('#destination-provider').val()),
            'recommended_date': $('#recommended-date').val(),
            'accepted_date': $('#accepted-date').val(),
            'completed_date': $('#completed-date').val(),
            'serviced_date': $('#serviced-date').val(),
            'referral_start_date': $('#referral-start-date').val(),
            'referral_end_date': $('#referral-end-date').val()
        }
        $.each(referral, function (key, value) {
            if (value === '' || value === null) {
                delete referral[key];
            }
            return referral;
        });
        $.post('/referrals/' + + $('#referral-id').val(), JSON.stringify(referral)).done(function () {
            showNotice('Updated Referral', 'Successfully updated referral.');
            $('#referral-form-modal').modal('toggle');
            location.reload();
        }).fail(function (data) {
            showNotice('Error', 'Failed to update referral.');
        });
    });

    $('#delete-referral').click(function (event) {
        event.preventDefault();
        $.ajax({
            url: '/referrals/' + $('#referral-id').val(),
            type: 'DELETE'
        }).done(function () {
            $('#referral-form-modal').modal('toggle');
            showNotice('Deleted Referral', 'Successfully deleted referral.');
        }).fail(function () {
            showNotice('Error', 'Failed to delete referral.');
        });
    });

    $('#create-referral').click(function (event) {
        event.preventDefault();
        const mciID = $('#mci-id').val();
        $('#mci-form-modal').modal('toggle');
        $('#referral-form-modal').modal('toggle');
        initReferralForm().then(function () {
            $('#user-id').val(mciID);
            $('#referral-date').val(getDate());
            $('#create-referral-buttons').show();
            $('#edit-referral-buttons').hide();
        }).catch(function () {
            showNotice('Error', 'Failed to load page.');
        });
    });

    $('#find-referral').click(function (event) {
        event.preventDefault();
        const mciID = $('#mci-id').val();
        const url = '/referrals/query/' + mciID;
        window.location.href = url;
    });
});