using TrakerBot.Application.Bookmakers.Commands;
using TrakerBot.Application.Bookmakers.DTOs;

namespace TrakerBot.Application.Bookmakers.Validators;

public class CreateBookmakerValidator : BaseBookmakerValidator<CreateBookmakerCommand.Command, CreateBookmakerDto>
{
    public CreateBookmakerValidator() : base(x => x.CreateBookmakerDto)
    {}
}
