$(function () {
    $.ajaxSetup({
        contentType: "application/json"
    });

    let appLoading = false;
    try {
        appLoading = true;
        preloadMCIFormFields().then(function () {
            $('#ethnicity-race').attr('size', $('#ethnicity-race option').length);
            appLoading = false;
        }).catch(function () {
            ;
        });
    } catch (e) {
        alert('Error loading page.');
    }

    async function preloadMCIFormFields() {
        await Promise.all([
            appendOption('/mci/gender', '#gender', 'gender'),
            appendOption('/mci/ethnicity', '#ethnicity-race', 'ethnicity_Race'),
            appendOption('/mci/education_level', '#education-level', 'education_level'),
            appendOption('/mci/employment_status', '#employment-status', 'employment_status'),
            appendOption('/mci/provider', '#provider', 'provider_name'),
            appendOption('/mci/country', '#country', 'country'),
            appendOption('/mci/state', '#state', 'state')
        ]);
    }

    function initMCIForm() {
        return new Promise(function (resolve, reject) {
            resolve(function () {
                $('#mci-form').trigger('reset');
            });
            reject(function () {
                alert('Cannot reset form.');
            });
        });
    }

    async function appendOption(url, id, key) {
        return $.getJSON(url, function (data) {
            $.each(data, function (_, value) {
                $(id).append(new Option(value[key], value[key]));
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
                console.log(data);
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
                console.log('Failed to load JavaScript.');
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
        $.post('/mci/users', JSON.stringify(user)).done(function () {
            alert('Done');
        }).fail(function (data) {
            alert('Fail');
            console.log(JSON.parse(data['responseText']));
        })
    });
});